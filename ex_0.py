# https://en.wikipedia.org/wiki/Z-order_curve
# https://www.forceflow.be/2013/10/07/morton-encodingdecoding-through-bit-interleaving-implementations/
# https://en.wikipedia.org/wiki/Octree
# https://en.wikipedia.org/wiki/SWAR
# https://github.com/jart/morton

def cmp_zorder(lhs, rhs) -> bool:
  """Compare z-ordering."""
  # Assume lhs and rhs array-like objects of indices.
  assert len(lhs) == len(rhs)
  # Will contain the most significant dimension.
  msd = 0
  # Loop over the other dimensions.
  for dim in range(1, len(lhs)):
      # Check if the current dimension is more significant
      # by comparing the most significant bits.
      if less_msb(lhs[msd] ^ rhs[msd], lhs[dim] ^ rhs[dim]):
          msd = dim
  return lhs[msd] < rhs[msd]


def less_msb(x: int, y: int) -> bool:
  return x < y and x < (x ^ y)


def test_cmp_zorder():
  # Test Case 1: lhs < rhs
  lhs, rhs = [1, 2, 3], [4, 5, 6]
  assert cmp_zorder(lhs, rhs), "Test Case 1 failed: expected lhs < rhs"

  # Test Case 2: rhs < lhs
  lhs, rhs = [4, 5, 6], [1, 2, 3]
  assert not cmp_zorder(lhs, rhs), "Test Case 2 failed: expected rhs < lhs"

  # Test Case 3: More complex case, similar higher order bits
  lhs, rhs = [15, 15, 14], [15, 15, 15]
  assert cmp_zorder(lhs, rhs), "Test Case 3 failed: expected lhs < rhs due to lower bits"

  # Test Case 4: lhs and rhs are equal
  lhs, rhs = [7, 7, 7], [7, 7, 7]
  assert not cmp_zorder(lhs, rhs), "Test Case 4 failed: expected comparison to return False as lhs == rhs"

  print("All test cases passed!")

# Running the test function
test_cmp_zorder()




def test_less_msb():
  # Test Case 1: Large numbers where x < y
  x = 2**60
  y = 2**60 + 1
  assert not less_msb(x, y), "Test Case 1 failed: x < y but MSB condition failed."

  # Test Case 2: Large numbers where x < y, focusing on MSB difference
  x = 2**130 - 1  # Max value for 130-bit integer minus 1
  y = 2**130  # Max value for 130-bit integer
  assert less_msb(x, y), "Test Case 2 failed: Expected x < y with clear MSB difference."

  # Test Case 3: x greater than y
  x = 2**128 + 2**64  # A large number with a significant MSB difference
  y = 2**64 + 1  # Smaller with respect to significant bits
  assert not less_msb(x, y), "Test Case 3 failed: x > y, should return False."

  # Test Case 4: Very close big values, determining factor is not MSB
  x = 2**256 - 100  # A very large number
  y = 2**256 - 50   # A slightly larger very large number
  assert less_msb(x, y), "Test Case 4 failed: x < y, very close values but should be true based on MSB."

  print("All test cases passed for less_msb with Big Integers!")

# Running the test function
test_less_msb()
