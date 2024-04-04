advent_of_code::solution!(5);
use itertools::Itertools;
use lazy_static::lazy_static;
use regex::Regex;

lazy_static! {
    static ref PATTERN: Regex = Regex::new(r"\d+",).unwrap();
}

#[derive(Clone, Debug)]
struct MapRange {
    destination: u64,
    source: u64,
    length: u64,
}

impl MapRange {
    fn get_target(&self, value: u64) -> Option<u64> {
        if (self.source..self.source + self.length).contains(&value) {
            Some(self.destination + value - self.source)
        } else {
            None
        }
    }
    fn get_prev(&self, value: u64) -> Option<u64> {
        if (self.destination..self.destination + self.length).contains(&value) {
            Some(self.source + value - self.destination)
        } else {
            None
        }
    }
}
#[derive(Clone, Debug)]
struct Map {
    ranges: Vec<MapRange>,
}

impl Map {
    fn get_target(&self, value: u64) -> u64 {
        for range in &self.ranges {
            if let Some(target) = range.get_target(value) {
                return target;
            }
        }
        value
    }
    fn get_prev(&self, value: u64) -> u64 {
        for range in &self.ranges {
            if let Some(target) = range.get_prev(value) {
                return target;
            }
        }
        value
    }
}

struct Maps {
    maps: Vec<Map>,
}

impl Maps {
    fn get_target(&self, value: u64) -> u64 {
        let mut val = value;
        for map in &self.maps {
            val = map.get_target(val);
        }
        val
    }
    fn get_prev(&self, value: u64) -> u64 {
        let mut val = value;
        for map in &self.maps {
            val = map.get_prev(val);
        }
        val
    }
}

fn parse_seeds(line: &str) -> Vec<u64> {
    PATTERN
        .find_iter(line)
        .map(|m| m.as_str().parse::<u64>().unwrap())
        .collect()
}

fn parse_maps(lines: &[&str]) -> Maps {
    let mut line_iter = lines.iter().filter(|l| !l.is_empty());
    let mut maps = Vec::new();
    let type_count = 7;
    for _ in 0..type_count {
        let mut ranges = Vec::new();
        loop {
            let line = line_iter.next();
            if line.is_none() || !line.unwrap().chars().next().unwrap().is_digit(10) {
                break;
            }
            let (destination, source, range) = PATTERN
                .find_iter(line.unwrap())
                .map(|m| m.as_str().parse().unwrap())
                .collect_tuple()
                .expect(line.unwrap());
            ranges.push(MapRange {
                destination,
                source,
                length: range,
            });
        }
        maps.push(Map { ranges });
    }

    Maps { maps }
}

pub fn part_one(input: &str) -> Option<u64> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let seeds = parse_seeds(lines[0]);
    let maps = parse_maps(&lines[3..]);
    seeds.iter().map(|s| maps.get_target(*s)).min()
}

#[derive(Debug)]
struct SeedRange {
    start: u64,
    length: u64,
}

fn parse_seeds_part_2(line: &str) -> Vec<SeedRange> {
    let mut seed_ranges = Vec::new();
    let values: Vec<u64> = PATTERN
        .find_iter(line)
        .map(|m| m.as_str().parse::<u64>().unwrap())
        .collect();

    for batch in values.chunks(2) {
        seed_ranges.push(SeedRange {
            start: batch[0],
            length: batch[1],
        })
    }
    seed_ranges
}
fn parse_maps_part_2(lines: &[&str]) -> Maps {
    let maps = parse_maps(lines);
    Maps {
        maps: maps.maps.iter().rev().cloned().collect(),
    }
}

pub fn part_two(input: &str) -> Option<u64> {
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let maps = parse_maps_part_2(&lines[3..]);
    let seed_ranges = parse_seeds_part_2(lines[0]);
    let mut counter: u64 = 0;
    loop {
        let val = maps.get_prev(counter);
        for seed_range in &seed_ranges {
            if (seed_range.start..seed_range.start + seed_range.length).contains(&val) {
                return Some(counter);
            }
        }
        counter += 1;
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let result = part_one(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(35));
    }

    #[test]
    fn test_part_two() {
        let result = part_two(&advent_of_code::template::read_file("examples", DAY));
        assert_eq!(result, Some(46));
    }
}
