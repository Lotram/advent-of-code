use regex::Regex;
use std::collections::HashMap;
advent_of_code::solution!(2);

pub fn part_one(input: &str) -> Option<u32> {
    let max_values = HashMap::from([("blue", 14), ("green", 13), ("red", 12)]);
    let main_re = Regex::new(r"\d+ \w+").unwrap();
    let game_re = Regex::new(r"Game (?P<game_id>\d+):").unwrap();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut sum = 0;
    for line in lines.iter() {
        let game_id: u32 = game_re
            .captures(line)
            .unwrap()
            .name("game_id")
            .unwrap()
            .as_str()
            .parse()
            .unwrap();
        let mut possible = true;
        let caps = main_re.captures_iter(line);
        for cap in caps {
            for c in cap.iter() {
                let v: Vec<&str> = c.unwrap().as_str().split(' ').collect();
                let count = v[0].parse::<u32>().unwrap();
                let color = v[1];
                if count > max_values[color] {
                    possible = false;
                    break;
                }
            }
        }
        if possible {
            sum += game_id;
        }
    }
    Some(sum)
}

pub fn part_two(input: &str) -> Option<u32> {
    let main_re = Regex::new(r"\d+ \w+").unwrap();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut sum: u32 = 0;
    for line in lines.iter() {
        let mut min_values = HashMap::from([("blue", 0), ("green", 0), ("red", 0)]);
        let caps = main_re.captures_iter(line);
        for cap in caps {
            for c in cap.iter() {
                let v: Vec<&str> = c.unwrap().as_str().split(' ').collect();
                let count: u32 = v[0].parse().unwrap();
                let color = v[1];
                if count > min_values[color] {
                    min_values.insert(color, count);
                }
            }
        }
        sum += min_values["blue"] * min_values["green"] * min_values["red"];
    }
    Some(sum)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(8));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(2286));
    }
}
