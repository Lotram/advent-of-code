advent_of_code::solution!(6);
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref PATTERN: Regex = Regex::new(r"\d+",).unwrap();
}
struct Race {
    time: u64,
    record: u64,
}

impl Race {
    fn get_len(&self) -> u64 {
        let discriminant: f64 = (self.time.pow(2) - 4 * self.record) as f64;
        let upper_root: f64 = (self.time as f64 + discriminant.sqrt()) / 2.0;
        let lower_root: f64 = (self.time as f64 - discriminant.sqrt()) / 2.0;
        let upper_bound = (upper_root - 1.0).ceil() as u64;
        let lower_bound = (lower_root + 1.0) as u64;
        return 1 + upper_bound - lower_bound;
    }
}

fn parse_line(line: &str) -> Vec<u64> {
    PATTERN
        .find_iter(line)
        .map(|m| m.as_str().parse::<u64>().unwrap())
        .collect()
}

// f(t) = - t*2 + t* Tm - R
// solutions = (Tm +- sqrt(Tm^2 - 4 * R)) / 2
pub fn part_one(input: &str) -> Option<u64> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let times: Vec<u64> = parse_line(lines[0]);
    let records: Vec<u64> = parse_line(lines[1]);
    let mut races = Vec::new();
    for (time, record) in times.iter().zip(records.iter()) {
        races.push(Race {
            time: *time,
            record: *record,
        })
    }
    let mut result: u64 = 1;
    for race in races {
        race.get_len();
        result *= race.get_len();
    }
    Some(result)
}

fn parse_line_part_2(line: &str) -> u64 {
    PATTERN
        .find_iter(line)
        .map(|m| m.as_str())
        .collect::<Vec<&str>>()
        .join("")
        .parse()
        .unwrap()
}

pub fn part_two(input: &str) -> Option<u64> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let time = parse_line_part_2(lines[0]);
    let record = parse_line_part_2(lines[1]);
    let race = Race { time, record };
    Some(race.get_len())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(288));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(71503));
    }
}
