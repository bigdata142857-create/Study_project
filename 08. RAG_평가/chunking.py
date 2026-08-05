import re


def is_section_start(line):

    patterns = [
        r"^\d+\.",
        r"^#\s*\d+\.",
        r"^##"
    ]

    return any(
        re.match(pattern, line)
        for pattern in patterns
    )


def create_parent_child(documents):

    parent_chunks = {}
    child_chunks = []

    parent_id = 0


    for file_name, text in documents.items():


        # ==========================
        # Parent = 문서 전체
        # ==========================

        parent_chunks[parent_id] = {

            "parent_id": parent_id,

            "title": file_name,

            "text": text

        }


        # ==========================
        # Child 생성
        # ==========================

        lines = text.splitlines()

        # 문서 헤더 제거
        while lines and "=" in lines[0]:
            lines.pop(0)

        current_section = []


        for line in lines:


            line = line.strip()


            if not line:
                continue


            # 새로운 Section 발견

            if is_section_start(line):


                if current_section:


                    child_chunks.append({

                        "chunk_id":
                            f"{parent_id}_{len(child_chunks)}",

                        "parent_id":
                            parent_id,

                        "text":
                            "\n".join(current_section)

                    })


                current_section = [line]


            else:

                current_section.append(line)



        # 마지막 section

        if current_section:


            child_chunks.append({

                "chunk_id":
                    f"{parent_id}_{len(child_chunks)}",

                "parent_id":
                    parent_id,

                "text":
                    "\n".join(current_section)

            })


        parent_id += 1



    return parent_chunks, child_chunks