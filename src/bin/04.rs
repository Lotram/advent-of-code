use lazy_static::lazy_static;
use regex::{Captures, Regex};
use std::ops::Range;
advent_of_code::solution!(4);

lazy_static! {
    static ref PATTERN: Regex =
        Regex::new(r"(?P<first_pair>\d+-\d+),(?P<second_pair>\d+-\d+)").unwrap();
}

fn get_range(caps: &Captures, name: &str) -> Range<u64> {
    let (start, end) = caps.name(name).unwrap().as_str().split_once('-').unwrap();
    Range {
        start: start.parse::<u64>().unwrap(),
        end: end.parse::<u64>().unwrap() + 1,
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut result = 0;
    for line in lines.iter() {
        let caps = PATTERN.captures(line).expect(line);
        let first_range = get_range(&caps, "first_pair");
        let second_range = get_range(&caps, "second_pair");
        if (first_range.start <= second_range.start && first_range.end >= second_range.end)
            || (second_range.start <= first_range.start && second_range.end >= first_range.end)
        {
            result += 1;
        }
    }
    Some(result)
}
fn ranges_overlap(range1: Range<u64>, range2: Range<u64>) -> bool {
    range1.contains(&range2.start) || range2.contains(&range1.start)
}

pub fn part_two(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut result = 0;
    for line in lines.iter() {
        let caps = PATTERN.captures(line).expect(line);
        let first_range = get_range(&caps, "first_pair");
        let second_range = get_range(&caps, "second_pair");
        if ranges_overlap(first_range, second_range) {
            result += 1;
        }
    }
    Some(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(2));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4));
    }
}
