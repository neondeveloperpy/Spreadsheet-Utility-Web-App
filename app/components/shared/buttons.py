from fasthtml.common import * 

def PrimaryButton(text, type="submit"):

    return Button(
        text, 

        type=type,

        cls="!w-fit bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded mt-1.5",

    )

# ! is tailwinds modifying to denote something important, in this case to overide pico css 

def SecondaryButton(text, type="submit"):

    return Button(
        text, 

        type=type,

        cls="!bg-blue-400 hover:bg-blue-300 text-white px-4 py-2 rounded",

    )
