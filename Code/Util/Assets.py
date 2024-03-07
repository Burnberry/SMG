from Code.Util.AssetClasses import ImageAsset


class Img:
    PygletLogo = ImageAsset("PygletLogo", "Assets/")

    CatWizard = ImageAsset("CatWizard", "Assets/Tiles/")

    BoxClosed = ImageAsset("BoxClosed", "Assets/Tiles/")
    BoxOpen = ImageAsset("BoxOpen", "Assets/Tiles/")
    BoxCrossed = ImageAsset("BoxCrossed", "Assets/Tiles/")
    FoodBowl = ImageAsset("FoodBowl", "Assets/Tiles/")
    FoodBowlCrossed = ImageAsset("FoodBowlCrossed", "Assets/Tiles/")
    Barrier = ImageAsset("Barrier", "Assets/Tiles/")
    ArrowRight = ImageAsset("ArrowRight", "Assets/Tiles/")
    ArrowLeft = ImageAsset("ArrowLeft", "Assets/Tiles/")


class Alpha:
    SymbolDict = {}
    for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789":
        SymbolDict[i] = ImageAsset(i, "Assets/Alphabet/")

    SymbolDict['!'] = ImageAsset("EMARK", "Assets/Alphabet/")
    SymbolDict['?'] = ImageAsset("QMARK", "Assets/Alphabet/")
    SymbolDict['.'] = ImageAsset("PERIOD", "Assets/Alphabet/")
    SymbolDict[','] = ImageAsset("COMMA", "Assets/Alphabet/")
    SymbolDict[':'] = ImageAsset("COLON", "Assets/Alphabet/")
    SymbolDict[';'] = ImageAsset("SEMICOLON", "Assets/Alphabet/")
    SymbolDict['+'] = ImageAsset("PLUS", "Assets/Alphabet/")
    SymbolDict['-'] = ImageAsset("MINUS", "Assets/Alphabet/")
    SymbolDict['/'] = ImageAsset("SLASH", "Assets/Alphabet/")
    SymbolDict['%'] = ImageAsset("PERCENT", "Assets/Alphabet/")
    SymbolDict['\''] = ImageAsset("QUOTATIONMARK", "Assets/Alphabet/")

    @staticmethod
    def get(symbol):
        symbol = symbol.upper()
        return Alpha.SymbolDict.get(symbol, None)
