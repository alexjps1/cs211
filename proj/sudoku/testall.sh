for file in data/*; do
    echo "$file"
    python3 sudoku.py "$file"
done
