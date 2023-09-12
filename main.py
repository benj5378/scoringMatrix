from pprint import pprint
from enum import Enum
from blosum import BLOSUM
import sys

# seq1 = " THEFASTCAT"
# seq2 = " THEFATCAT"

scoringTable = BLOSUM(62)
gapPenalty: str = -8


class Origin(Enum):
    UpperLeft = 0
    Left = 1
    Upper = 2


class ScoreCell:
    
    previous: Origin = -1
    value: int = -999

    def __str__(self):
        # return str(0)
        return str(self.value)
    
    def __repr__(self):
        return "ScoringCell: " + str(self.value)

    def calculate(self, previous: Origin, previousValue: int, letters: str):
        if len(letters) != 2:
            raise ValueError("letters")
        self.previous = previous

        if previous == Origin.Left or previous == Origin.Upper:
            self.value = previousValue + gapPenalty
        else:
            self.value = int(previousValue + scoringTable[letters[0]][letters[1]])
        
        return self.value

class ScoreTable:
    scores: list[list[ScoreCell]] = []
    rowIndex: int
    columnIndex: int

    def __init__(self, seq1, seq2):
        self.seq1: str = " " + seq1
        self.seq2: str = " " + seq2
        for row in self.seq1:
            self.scores.append([])
            rowContainer = self.scores[-1]
            for column in self.seq2:
                rowContainer.append(ScoreCell())

        self.scores[0][0].value = 0

    def __str__(self):
        lines = ""
        firstRow = True
        for rowLetter, row in zip(self.seq1, self.scores):
            if firstRow:
                line = "          "
                for letter in self.seq2[1:]:
                    line = line + f"   {letter:>7}"
                firstRow = False
                lines = lines + line + "\n"

            lines = lines + "\n"
            line = " "
            previousCell = ScoreCell()
            firstCell = True
            for cell in row:
                if previousCell.previous == Origin.UpperLeft:
                    line = line + "   "
                if cell.previous == Origin.Upper:
                    line = line + "       "
                if cell.previous == Origin.Upper:
                    line = line + " ⇓ "
                elif cell.previous == Origin.UpperLeft:
                    line = line + "    ⇘  "
                else:
                    line = line + "   "
                previousCell = cell
            lines = lines + line + "\n"
            lines = lines + "\n"

            firstCell = True
            for cell in row:
                if firstCell:
                    line = rowLetter
                    firstCell = False
                if cell.previous == Origin.Left:
                    line = line + " ⇒ " # "⭨⭢⭣"
                else:
                    line = line + "   "
                line = line + f"{str(cell.value):>7}"
            lines = lines + line + "\n"


        return lines

    def calculate(self):
        for self.rowIndex, row in enumerate(self.scores):
            for self.columnIndex, cell in enumerate(row):
                if self.rowIndex == 0 and self.columnIndex == 0:
                    continue
                elif self.columnIndex == 0:
                    self.calculateCell(cell, Origin.Upper)
                elif self.rowIndex == 0:
                    self.calculateCell(cell, Origin.Left)
                else:
                    origin: Origin
                    # print(
                    #     str(self.calculateCell(cell, Origin.Upper)) + "\n" +
                    #     str(self.calculateCell(cell, Origin.Left)) + "\n" +
                    #     str(self.calculateCell(cell, Origin.UpperLeft))
                    # )
                    maxScore = max(self.calculateCell(cell, Origin.Upper), self.calculateCell(cell, Origin.Left), self.calculateCell(cell, Origin.UpperLeft))

                    if maxScore == self.calculateCell(cell, Origin.Upper):
                        origin = Origin.Upper
                    elif maxScore == self.calculateCell(cell, Origin.Left):
                        origin = Origin.Left
                    else:
                        origin = Origin.UpperLeft

                    r = self.calculateCell(cell, origin)
                    # print(f"row: {self.rowIndex}, column: {self.columnIndex}, value: {r}, previous {cell.previous}, origin: {origin}")

    def calculateCell(self, cell: ScoreCell, previous: Origin) -> int:
        return cell.calculate(
            previous,
            self.getCell(previous).value,
            self.seq1[self.rowIndex] + self.seq2[self.columnIndex]
        )

    def getCell(self, origin: Origin):
        if origin == Origin.Upper:
            return self.scores[self.rowIndex - 1][self.columnIndex]
        if origin == Origin.Left:
            return self.scores[self.rowIndex][self.columnIndex - 1]
        if origin == Origin.UpperLeft:
            return self.scores[self.rowIndex - 1][self.columnIndex - 1]


if __name__ == "__main__":
    seq1: str
    seq2: str
    if len(sys.argv) > 1:
        seq1 = sys.argv[1]
        seq2 = sys.argv[2]
    else:
        seq1 = "THEFATCAT"
        seq2 = "THEFASTCAT"
    
    table = ScoreTable(seq1, seq2)
    table.calculate()
    print(str(table))
