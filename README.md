# maze_printer
Generates PDFs with mazes

# Usage
The script can be run with no arugments, or any number of supported arguments
so long as they are in the correct order:

`python maze_printer.py`

`python maze_printer.py [total_images] [images_per_row] [images_per_column] [output_name]`

- total_images: The total number of mazes you want
  - Default: 4
- images_per_row: number of mazes in each row on the page
  - Default: 2
- images_per_col: number of mazes in each column on the page
  - Default: 2
- output_name: PDF name. NOTE: the ".pdf" extension is added automatically
  - Default: 'maze'