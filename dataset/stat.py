import os
import javalang

def count_classes_and_methods(repo_path: str):
    class_count = 0
    method_count = 0
    file_count = 0
    parse_errors = 0

    for root, _, files in os.walk(repo_path):
        for file in files:
            if not file.endswith(".java"):
                continue

            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()

                tree = javalang.parse.parse(code)
                file_count += 1

                for _, node in tree.filter(javalang.tree.TypeDeclaration):
                    if isinstance(node, (
                        javalang.tree.ClassDeclaration,
                        javalang.tree.InterfaceDeclaration,
                        javalang.tree.EnumDeclaration
                    )):
                        class_count += 1

                        for body_decl in node.body:
                            if isinstance(body_decl, (
                                javalang.tree.MethodDeclaration,
                                javalang.tree.ConstructorDeclaration
                            )):
                                method_count += 1

            except Exception:
                parse_errors += 1
                continue

    return {
        "files_parsed": file_count,
        "class_count": class_count,
        "method_count": method_count,
        "parse_errors": parse_errors
    }


if __name__ == "__main__":
    repo = "SmellRefactoring/dataset/nanojson-master"
    stats = count_classes_and_methods(repo)
    print(stats)
