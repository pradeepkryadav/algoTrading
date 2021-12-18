## unzip all file into thier folders 
find . -name "*.zip" | while read filename; do unzip -o -d "`dirname "$filename"`" "$filename"; done;

## removing spaces in folder name 
for directory in **; do
    if [[ -d $directory ]] && [[ -w $directory ]]; then
        mv -- "$directory" "${directory// /-}"
    fi
done

## remaning file name 
for folder in *; do
  if [ -d "$folder" ]; then
    cd "$folder"
    for file in *.txt; do
      mv -- "$file" "${folder}_$file"
    done
    cd ..
  fi
done
