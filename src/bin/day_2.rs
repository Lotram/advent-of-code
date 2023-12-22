use std::error::Error;
use std::fs;
enum Outcome {
    Win,
    Lose,
    Draw,
}

impl Outcome {
    fn value(&self) -> u32 {
        match self {
            Outcome::Lose => 0,
            Outcome::Draw => 3,
            Outcome::Win => 6,
        }
    }
    fn from_char(c: char) -> Outcome {
        match c {
            'X' => Outcome::Lose,
            'Y' => Outcome::Draw,
            'Z' => Outcome::Win,
            _ => panic!("Invalid character: {}", c),
        }
    }
}
#[derive(Copy, Clone)]
enum Sign {
    Rock,
    Paper,
    Scissors,
}
impl Sign {
    fn value(&self) -> u32 {
        match self {
            Sign::Rock => 1,
            Sign::Paper => 2,
            Sign::Scissors => 3,
        }
    }

    fn from_char(c: char) -> Sign {
        match c {
            'A' => Sign::Rock,
            'B' => Sign::Paper,
            'C' => Sign::Scissors,
            _ => panic!("Invalid character: {}", c),
        }
    }
}
struct Round {
    opponent: Sign,
    outcome: Outcome,
}

impl Round {
    fn me(&self) -> Sign {
        match (&self.outcome, &self.opponent) {
            (Outcome::Win, Sign::Rock) => Sign::Paper,
            (Outcome::Win, Sign::Paper) => Sign::Scissors,
            (Outcome::Win, Sign::Scissors) => Sign::Rock,
            (Outcome::Lose, Sign::Rock) => Sign::Scissors,
            (Outcome::Lose, Sign::Paper) => Sign::Rock,
            (Outcome::Lose, Sign::Scissors) => Sign::Paper,
            _ => self.opponent,
        }
    }
    fn score(&self) -> u32 {
        self.outcome.value() + self.me().value()
    }
    fn from_str(line: &str) -> Round {
        let mut iter = line.split(" ");
        let opponent = iter.next().expect(line).chars().next().expect(line);
        let outcome = iter.next().expect(line).chars().next().expect(line);
        Round {
            opponent: Sign::from_char(opponent),
            outcome: Outcome::from_char(outcome),
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    // Read the input from a file
    let input = fs::read_to_string("data.txt").expect("Failed to read input file");

    // Split the input into lines
    let mut total_score: u32 = 0;
    let lines: Vec<&str> = input.trim().split("\n").collect();
    for line in lines.iter() {
        let round = Round::from_str(line);
        total_score += round.score();
    }
    println!("The total score is {}.", total_score);
    Ok(())
}
