#!/usr/bin/env bash

find_project_root() {
    local dir="$PWD"

    while [ "$dir" != "/" ]; do
        if [ -f "$dir/.gitignore" ] || [ -d "$dir/.git" ]; then
            echo "$dir"
            return 0
        fi
        dir="$(dirname "$dir")"
    done

    if [ -f "/.gitignore" ] || [ -d "/.git" ]; then
        echo "/"
        return 0
    fi
    
    echo "Error: Project root (with .gitignore or .git) not found." >&2
    return 1
}

# Comp
PROJECT_ROOT=$(find_project_root)
if [ $? -eq 0 ]; then
    echo "Found project root at: $PROJECT_ROOT"

    echo "Compiling requirements"

    pipreqs "$PROJECT_ROOT" --ignore .venv --force

    echo "Done"
fi