use lazy_static::lazy_static;
use regex::Regex;
use std::collections::HashSet;
advent_of_code::solution!(4);

lazy_static! {
    static ref PATTERN: Regex = Regex::new(
        r"Card\ +(?P<card_id>\d+): (?P<winning>(?: *\d+ *)+) \| (?<my_numbers>(?: *\d+ *)+)",
    )
    .unwrap();
}
pub fn part_one(input: &str) -> Option<u32> {
    let mut sum = 0;
    let lines: Vec<&str> = input.trim().split("\n").collect();
    for line in lines.iter() {
        let intersection = winning_count(line);
        if intersection > 0 {
            let two: u32 = 2;
            sum += two.pow((intersection - 1).try_into().unwrap());
        }
    }
    Some(sum)
}

fn winning_count(line: &&str) -> u32 {
    let capture = PATTERN.captures(line).expect(line);
    // let card_id: u32 = capture.name("card_id").unwrap().as_str().parse().unwrap();
    let winning_numbers: HashSet<u32> = capture
        .name("winning")
        .unwrap()
        .as_str()
        .split(' ')
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().unwrap())
        .collect();

    let my_numbers: HashSet<u32> = capture
        .name("my_numbers")
        .unwrap()
        .as_str()
        .split(' ')
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().unwrap())
        .collect();
    (&winning_numbers & &my_numbers).len() as u32
}

pub fn part_two(input: &str) -> Option<u32> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut copies: Vec<u32> = vec![1; lines.len()]; // We start with 1 copy of each card

    for (idx, line) in lines.iter().enumerate() {
        let copies_count = copies[idx];
        let count = winning_count(line);
        for next_card in 0..count {
            copies[idx + next_card as usize + 1] += copies_count
        }
    }
    Some(copies.iter().sum())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(13));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(30));
    }
}
