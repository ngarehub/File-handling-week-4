from pathlib import Path
import sys
import re

def get_input_file():
    """Ask for a file until it can be read, or exit after failure."""
    while True:
        path = Path(input("Enter input filename: ").strip()).expanduser()
        try:
            with path.open("r", encoding="utf-8") as f:
                return path, f.read()
        except FileNotFoundError:
            print("❌ File not found. Try again.")
        except PermissionError:
            print("❌ Permission denied. Try again.")
        except UnicodeDecodeError:
            print("❌ File is not plain text. Try again.")
        except Exception as e:
            print(f"❌ Error: {e}")
            sys.exit(1)

def get_output_file(input_path: Path):
    """Suggests a default output file, lets user override."""
    default = input_path.with_name(input_path.stem + ".modified" + input_path.suffix)
    out_str = input(f'Enter output filename [default: {default.name}]: ').strip()
    return Path(out_str).expanduser() if out_str else default

def transform(text: str) -> str:
    """Modify the text: trim spaces, collapse whitespace, uppercase, add line numbers."""
    lines = text.splitlines()
    result = []
    for i, line in enumerate(lines, 1):
        cleaned = re.sub(r"\s+", " ", line.strip())
        result.append(f"{i:04d}: {cleaned.upper()}")
    return "\n".join(result) + ("\n" if text.endswith("\n") else "")

def main():
    print("🔧 File Modifier\n")
    in_path, content = get_input_file()
    modified = transform(content)
    out_path = get_output_file(in_path)

    try:
        with out_path.open("w", encoding="utf-8") as f:
            f.write(modified)
        print(f"✅ Done! Saved to {out_path}")
    except Exception as e:
        print(f"❌ Could not write file: {e}")

if __name__ == "__main__":
    main()
