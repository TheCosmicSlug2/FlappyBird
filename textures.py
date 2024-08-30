import pygame as pg

pg.init()

textures_path = "ressources/textures/"
texture_ext = ".png"



def convert_to_pygame_texture(texture_path: str, dims: tuple) -> pg.surface:
    """
    On prend le chemin de l'image
    On la convertit en objet pygame
    On dessine cet objet sur une surface pour pouvoir "blitter" directement sur écran
    (Impossible de blitter une image pygame)
    On retourne la surface
    """

    img = pg.image.load(texture_path).convert_alpha()
    img = pg.transform.scale(img, dims)
    surface = pg.Surface(dims, pg.SRCALPHA)
    surface.blit(img, (0, 0))
    return surface


def load_textures(liste_texture_name_size: list[tuple[int, tuple[int, int]]]) -> dict:


    # 1er élément de ce dictionnaire utilisé pour dessiner le cache du décor
    dic_textures = {}

    for texture_name, texture_dims in liste_texture_name_size:
        dic_textures[texture_name] = convert_to_pygame_texture(
           textures_path + texture_name + texture_ext, texture_dims
        )
    """

    # Pour chaque idx_de_texture, nom_de_la_texture
    for texture_ID, texture_name in dic_path.items():
        # Pour chaque idx_de_liste de la liste texture_size
        for texture_family_idx in range(len(texture_size)):
            # Si l'idx est 0 : dims = cellsizex, cellsizey (dimensions possiblement non constantes)
            if texture_family_idx == 0:
                dic_textures[texture_ID] = convert_to_pygame_texture(dir_textures_path + texture_name + texture_ext,
                                                                     dic_textures["dims"])
            # Sinon : dimensions sont prédéfinies (celles du joueur ou des ennemis)
            elif texture_name in texture_size[texture_family_idx]:
                dims = texture_size[texture_family_idx][-1]
                dic_textures[texture_ID] = convert_to_pygame_texture(dir_textures_path + texture_name + texture_ext,
                                                                     dims)

    """
    print("Textures crées")
    return dic_textures
