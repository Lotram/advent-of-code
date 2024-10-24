from .utils import get_example_path, get_solution_path


RUST_TEMPLATE = r"""advent_of_code::solution!(DAY_NUMBER);

pub fn part_one(input: &str) -> Option<u32> {
    None
}

pub fn part_two(input: &str) -> Option<u32> {
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, None);
    }
}
"""

PYTHON_TEMPLATE = r"""def part_1(text, example: bool = False):
    result = None
    return result


def part_2(text, example: bool = False):
    result = None
    return result
"""


def scaffold(day, year):
    solution = get_solution_path(day, year)
    solution.write_text(PYTHON_TEMPLATE)
    print(f'Created python file "{solution}"')

    example = get_example_path(day, year)
    example.touch()
    print(f'Created empty example file "{example}"')

    print(f"🎄 Type `pdm solve {day}` to run your solution.")
