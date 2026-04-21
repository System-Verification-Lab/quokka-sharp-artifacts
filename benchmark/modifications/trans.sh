for file in ../algorithm/algo_grover/*.qasm
do
    echo "Processing $file"
    python3 qasm_trans.py "$file"
done

