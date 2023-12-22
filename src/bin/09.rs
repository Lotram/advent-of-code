advent_of_code::solution!(9);
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref PATTERN: Regex = Regex::new(r"(-?\d+)",).unwrap();
}
fn parse_line(line: &str) -> Vec<i64> {
    PATTERN
        .find_iter(line)
        .map(|m| m.as_str().parse::<i64>().unwrap())
        .collect()
}

fn predict(values: Vec<i64>) -> i64 {
    let new_values = Vec::new();
    let mut current_values: Vec<i64> = values.clone();
    for idx in 0..values.len() {
        new_values.push(values[idx + 1] -values[idx]);
    }
    1

}

pub fn part_one(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    for line in lines {
        let values = parse_line(line);
    }
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
