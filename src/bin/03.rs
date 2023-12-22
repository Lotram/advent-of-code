use itertools::any;
use regex::Regex;
use std::cmp::max;
use std::collections::{HashMap, HashSet};
advent_of_code::solution!(3);

pub fn part_one(input: &str) -> Option<u32> {
    let symbol_pattern = Regex::new(r"[^\d.\n]").unwrap();
    let digit_pattern = Regex::new(r"\d+").unwrap();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut possible_values: HashSet<(usize, usize)> = HashSet::new();
    for (row_idx, line) in lines.iter().enumerate() {
        for match_ in symbol_pattern.find_iter(line) {
            for column in max(0, match_.start() - 1)..match_.end() + 1 {
                for row in max(row_idx - 1, 0)..(row_idx + 2) {
                    possible_values.insert((row, column));
                }
            }
        }
    }
    let mut sum = 0;
    for (row_idx, line) in lines.iter().enumerate() {
        for match_ in digit_pattern.find_iter(line) {
            let value = match_.as_str().parse::<u32>().unwrap();
            if any(match_.range(), |col| {
                possible_values.contains(&(row_idx, col))
            }) {
                sum += value;
            }
        }
    }

    Some(sum)
}

pub fn part_two(input: &str) -> Option<u32> {
    let star_pattern = Regex::new(r"\*").unwrap();
    let digit_pattern = Regex::new(r"\d+").unwrap();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut possible_values: HashMap<(usize, usize), (usize, u32)> = HashMap::new();

    for (row_idx, line) in lines.iter().enumerate() {
        for (idx, match_) in digit_pattern.find_iter(line).enumerate() {
            for column in match_.start()..match_.end() {
                possible_values.insert(
                    (row_idx, column),
                    (idx, match_.as_str().parse::<u32>().unwrap()),
                );
            }
        }
    }
    let mut sum = 0;
    for (row_idx, line) in lines.iter().enumerate() {
        for match_ in star_pattern.find_iter(line) {
            let mut hits = HashMap::new();
            for column in max(0, match_.start() as i32 - 1)..match_.end() as i32 + 1 {
                for row in max(row_idx as i32 - 1, 0)..(row_idx as i32 + 2) {
                    let value = possible_values.get(&(row as usize, column as usize));
                    if value.is_some() {
                        hits.insert((row, value.unwrap().0), value.unwrap().1);
                    }
                }
            }
            if hits.len() == 2 {
                let mut product = 1;
                for value in hits.values() {
                    product *= value;
                }
                sum += product;
            }
        }
    }

    Some(sum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(4361));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(467835));
    }
}
