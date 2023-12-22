advent_of_code::solution!(3);
use std::collections::{HashMap, HashSet};
pub fn part_one(input: &str) -> Option<u32> {
    let mut total_score: u32 = 0;
    let value_by_char = build_value_map();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    for line in lines.iter() {
        let chars: Vec<char> = line.chars().collect();
        let length = chars.len();
        let first_half = chars[..length / 2].iter().cloned().collect::<HashSet<_>>();
        let second_half = chars[length / 2..].iter().cloned().collect::<HashSet<_>>();
        let shared_element = first_half
            .intersection(&second_half)
            .into_iter()
            .next()
            .expect("The hashset should not be empty");
        total_score += value_by_char
            .get(shared_element)
            .copied()
            .expect("Value should be present");
    }
    println!("The total value is {}.", total_score);
    Some(total_score)
}

fn build_value_map() -> HashMap<char, u32> {
    let mut letters: Vec<char> = (b'a'..=b'z').map(char::from).collect();
    letters.extend((b'A'..=b'Z').map(char::from).collect::<Vec<_>>());
    let numbers: Vec<u32> = (1..=52).collect();

    letters
        .into_iter()
        .zip(numbers.into_iter())
        .collect::<HashMap<char, u32>>()
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut total_score: u32 = 0;
    let value_by_char = build_value_map();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    for group in lines.chunks(3) {
        let mut elements: HashSet<char> = HashSet::new();
        for line in group.iter() {
            let chars = HashSet::from_iter(line.chars());
            if elements.is_empty() {
                elements = chars;
            } else {
                elements = elements.intersection(&chars).copied().collect();
            }
        }

        let shared_element = elements
            .into_iter()
            .next()
            .expect("The hashset should not be empty");

        total_score += value_by_char
            .get(&shared_element)
            .copied()
            .expect("Value should be present");
    }
    println!("The total value is {}.", total_score);
    Some(total_score)
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
