use std::fs;

fn main() {
    // Read the input from a file
    let input = fs::read_to_string("data.txt").expect("Failed to read input file");

    // Split the input into lines
    let lines: Vec<&str> = input.trim().split("\n\n").collect();

    // Initialize variables to keep track of the top three Elves and their total calories
    let mut top_elves: [(usize, u32); 3] = [(0, 0), (0, 0), (0, 0)];

    // Iterate over each Elf's inventory
    for (elf_num, line) in lines.iter().enumerate() {
        // Split the line into individual calorie values
        let calories: Vec<u32> = line
            .trim()
            .split("\n")
            .map(|s| s.parse().expect("Invalid calorie value"))
            .collect();

        // Calculate the total calories for the current Elf
        let total_calories: u32 = calories.iter().sum();

        // Update the top three Elves if necessary
        if total_calories > top_elves[0].1 {
            top_elves[2] = top_elves[1];
            top_elves[1] = top_elves[0];
            top_elves[0] = (elf_num + 1, total_calories);
        } else if total_calories > top_elves[1].1 {
            top_elves[2] = top_elves[1];
            top_elves[1] = (elf_num + 1, total_calories);
        } else if total_calories > top_elves[2].1 {
            top_elves[2] = (elf_num + 1, total_calories);
        }
    }

    // Calculate the total calories of the top three Elves
    let total_calories_top_elves: u32 = top_elves.iter().map(|(_, calories)| *calories).sum();

    // Print the result
    println!(
        "The total calories carried by the top three Elves is {}.",
        total_calories_top_elves
    );
}
