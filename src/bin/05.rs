advent_of_code::solution!(5);
use regex::Regex;

fn build_stacks(lines: &[&str]) -> Vec<Vec<char>> {
    let mut stacks = Vec::new();
    for line in lines.iter().rev() {
        let chars: Vec<char> = line.chars().skip(1).step_by(4).collect();
        for (idx, char) in chars.iter().enumerate() {
            if char.is_digit(10) {
                stacks.push(Vec::new());
            } else if !(*char == ' ') {
                stacks[idx].push(*char);
            }
        }
    }
    stacks
}

struct Move {
    count: u32,
    from: u32,
    to: u32,
}

fn build_moves(lines: &[&str]) -> Vec<Move> {
    let re = Regex::new(r"move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)").unwrap();
    let mut moves = Vec::new();
    for line in lines {
        let caps = re.captures(line);
        if caps.is_none() {
            continue;
        }
        let caps = caps.unwrap();
        moves.push(Move {
            count: caps.name("count").expect(&line).as_str().parse().unwrap(),
            from: caps.name("from").unwrap().as_str().parse().unwrap(),
            to: caps.name("to").unwrap().as_str().parse().unwrap(),
        })
    }
    moves
}

pub fn part_one(input: &str) -> Option<String> {
    let lines: Vec<&str> = input.split("\n").collect();
    let empty_string_index = lines.iter().position(|s| s.is_empty()).unwrap();
    let mut stacks = build_stacks(&lines[..empty_string_index]);

    let moves = build_moves(&lines[empty_string_index + 1..]);
    for move_ in moves {
        for _ in 0..move_.count {
            let item = stacks[(move_.from - 1) as usize].pop();
            stacks[(move_.to - 1) as usize].push(item.unwrap());
        }
    }
    let mut result = String::new();
    for stack in stacks {
        result.push(stack[stack.len() - 1]);
    }
    Some(result)
}

pub fn part_two(input: &str) -> Option<String> {
    let lines: Vec<&str> = input.split("\n").collect();
    let empty_string_index = lines.iter().position(|s| s.is_empty()).unwrap();
    let mut stacks = build_stacks(&lines[..empty_string_index]);

    let moves = build_moves(&lines[empty_string_index + 1..]);
    for move_ in moves {
        let stack_index = (move_.from - 1) as usize;
        let start_index = stacks[stack_index]
            .len()
            .saturating_sub(move_.count as usize);
        let items = &stacks[(move_.from - 1) as usize]
            .drain(start_index..)
            .collect::<Vec<char>>();
        stacks[(move_.to - 1) as usize].extend(items);
    }
    let mut result = String::new();
    for stack in stacks {
        result.push(stack[stack.len() - 1]);
    }
    Some(result)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some("CMZ".to_string()));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some("MCD".to_string()));
    }
}
