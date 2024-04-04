advent_of_code::solution!(10);



pub fn part_one(input: &str) -> Option<u32> {
    let mut rows = Vec::new();
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut start: (usize, usize) = (0, 0);
    for (row_id, line) in lines.iter().enumerate() {
        let row: Vec<char> = line.chars().collect();
        let has_s = &row.iter().position(|c| *c == 'S');
        if let Some(pos) = has_s{
            start = (row_id, pos.clone());
        }
        rows.push(row);
    }
    let  (mut row, mut col) = start;
    loop {
        for row_idx in row.saturating_sub(1)..row+1 {
            for col_idx in col.saturating_sub(1)..col+1 {
                if (col_idx == 0 && row_idx == 0) || rows[row_idx][col_idx] == '.' {
                    continue
                }
            }
        }
    }
    None
}

pub fn part_two(input: &str) -> Option<u32> {
    None
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
