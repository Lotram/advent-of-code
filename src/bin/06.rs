use std::collections::HashSet;
use std::collections::VecDeque;
advent_of_code::solution!(6);

const PACKET_SIZE: usize = 4;
const MESSAGE_SIZE: usize = 14;

fn are_different(size: usize, chars: &VecDeque<char>) -> bool {
    chars.clone().into_iter().collect::<HashSet<char>>().len() == size
}

fn solve(input: &str, size: usize) -> Option<u32> {
    let mut chars: Vec<char> = input.split("\n").next().unwrap().chars().rev().collect();
    let mut char_queue: VecDeque<char> = VecDeque::new();
    for _ in 0..size {
        char_queue.push_back(chars.pop().unwrap());
    }

    let mut counter: u32 = size as u32;
    loop {
        if are_different(size, &char_queue) {
            return Some(counter);
        }
        counter += 1;
        char_queue.pop_front();
        char_queue.push_back(chars.pop().unwrap());
    }
}

pub fn part_one(input: &str) -> Option<u32> {
    return solve(&input, PACKET_SIZE);
}

pub fn part_two(input: &str) -> Option<u32> {
    return solve(&input, MESSAGE_SIZE);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(7));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(19));
    }
}
