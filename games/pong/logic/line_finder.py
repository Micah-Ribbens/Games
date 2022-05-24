class LineFinder:
    """Finds all the lines inside a file"""

    def get_lines(file_path):
        """ summary: iterates over the entire file to find the lines
            params:
                file_path: String; the path to the file
            returns: List of String; the lines in the file
        """
        current_line = ""
        lines = []
        enter = """
"""
        file = open(file_path, "r")

        for ch in file.read():
            if ch == enter:
                lines.append(current_line)
                current_line = ""

            else:
                current_line += ch

        lines.append(current_line)
        file.close()
        return lines