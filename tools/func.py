
from typing import Dict, List, Optional

#xfill
def xfill(
            num : int,
            *,
            length : Optional[int],
            fill_char : Optional[str] = "|"
            #cover_style : None =  "1"

    ):
        """A function that can show the numeber
        with a bar.

        Parameters
        -----------
            num: `int`
                The number of the rate.

            length: `int | None`
                The lenght of the bar.

            fill_char: `any`
                The filler of the box.

        ### Example:

        ```python
            >>> x = xfill(78, length = "|", fill_char = 20)
            ...  print(x)
            >>> [|||||||||||||||     ]
        ```

        
        """
        if length is None:
            length = 20
        if fill_char is None:
            fill_char = "|"
        box = 100/length  # the rate of the ouput box
        tmp = "[" # mabe can use cover_style to change '[ ]' or '{ }' ect...
        for _ in range(int(num/box)):# number of filler
            tmp = tmp + fill_char
        for _ in range(length-int(num/box)):# number of spece
            tmp = tmp + " "
        return tmp + "]"
