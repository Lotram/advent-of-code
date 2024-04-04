use std::collections::HashMap;

advent_of_code::solution!(1);

pub fn part_one(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut total: u32 = 0;
    for line in lines.iter() {
        let chars: Vec<char> = line.chars().filter(|x| x.is_digit(10)).collect();
        let length = chars.len();
        let number = String::from_iter([chars[0], chars[length - 1]]);
        total += number.parse::<u32>().unwrap();
    }

    Some(total)
}

pub fn part_two(input: &str) -> Option<u32> {
    let numbers = HashMap::from([
        ("one", "1"),
        ("two", "2"),
        ("three", "3"),
        ("four", "4"),
        ("five", "5"),
        ("six", "6"),
        ("seven", "7"),
        ("eight", "8"),
        ("nine", "9"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
    ]);

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut total: u32 = 0;
    for line in lines.iter() {
        let length = line.len();
        let mut first_digit: Option<&str> = None;
        let mut last_digit: Option<&str> = None;
        let mut first_digit_idx = length + 1;
        let mut last_digit_idx = 0;
        for (number, digit) in numbers.iter() {
            let first_index = line.find(number);
            match first_index {
                None => continue,
                Some(idx) => {
                    if idx < first_digit_idx {
                        first_digit_idx = idx;
                        first_digit = Some(digit);
                    }
                }
            }
            let last_index = line.rfind(number);
            match last_index {
                None => continue,
                Some(idx) => {
                    if (idx == 0 && last_digit_idx == 0) || idx > last_digit_idx {
                        last_digit_idx = idx;
                        last_digit = Some(digit);
                    }
                }
            }
        }

        let number = String::from_iter([first_digit.unwrap(), last_digit.unwrap()]);
        total += number.parse::<u32>().unwrap();
    }

    Some(total)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(142));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file_part(
            "examples", DAY, 2,
        ));
        assert_eq!(result, Some(281));
    }
}
