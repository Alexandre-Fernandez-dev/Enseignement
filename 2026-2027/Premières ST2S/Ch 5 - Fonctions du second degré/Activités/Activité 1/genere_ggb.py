#!/usr/bin/env python3
"""Génère 1ST2S_Ch5_Parabole.ggb (GeoGebra) pour l'activité 1 et le cours du chapitre 5.

Contenu :
- curseurs a, x_1, x_2 et la parabole f(x) = a (x - x_1)(x - x_2),
  réglés au départ sur le dauphin : a = -0,5 ; x_1 = 1 ; x_2 = 7 ;
- les racines R_1 et R_2 sur l'axe des abscisses ;
- deux textes sous les curseurs : la forme factorisée générale, puis la formule
  de f avec les valeurs des curseurs (mise à jour quand on les déplace) ;
- les points du tableau de valeurs du dauphin (liste T) ;
- g : la forme développée a x² + b x + c, calculée à partir des curseurs
  (la vue Algèbre affiche ses coefficients) ;
- masqués au départ (à afficher dans la vue Algèbre pour la séance 5) :
  le curseur c et la parabole h(x) = a x² + c.

Relancer : python3 genere_ggb.py (dans ce dossier).
"""
import zipfile

def curseur(nom, val, mn, mx, pas, y, visible=True):
    return f"""<element type="numeric" label="{nom}">
	<value val="{val}"/>
	<slider min="{mn}" max="{mx}" absoluteScreenLocation="true" width="220" x="40" y="{y}" fixed="true" horizontal="true" showAlgebra="true"/>
	<lineStyle thickness="10" type="0" typeHidden="1"/>
	<animation step="{pas}" speed="1" type="0" playing="false"/>
	<show object="{'true' if visible else 'false'}" label="true"/>
	<objColor r="0" g="0" b="0" alpha="0.1"/>
	<layer val="0"/>
	<labelMode val="1"/>
</element>
"""

def fonction(nom, exp, rgb, visible=True, epaisseur=7):
    r, g, b = rgb
    return f"""<expression label="{nom}" exp="{exp}" type="function"/>
<element type="function" label="{nom}">
	<show object="{'true' if visible else 'false'}" label="true"/>
	<objColor r="{r}" g="{g}" b="{b}" alpha="0"/>
	<layer val="0"/>
	<labelMode val="0"/>
	<fixed val="true"/>
	<lineStyle thickness="{epaisseur}" type="0" typeHidden="1" opacity="204"/>
</element>
"""

def texte(nom, exp, y, rgb=(0, 0, 0), latex=False):
    r, g, b = rgb
    return f"""<expression label="{nom}" exp="{exp}"/>
<element type="text" label="{nom}">
	<show object="true" label="false"/>
	<objColor r="{r}" g="{g}" b="{b}" alpha="0"/>
	<layer val="0"/>
	<labelMode val="0"/>
	<fixed val="true"/>
	<isLaTeX val="{'true' if latex else 'false'}"/>
	<absoluteScreenLocation x="40" y="{y}"/>
</element>
"""

def point(nom, exp, rgb, taille=6):
    r, g, b = rgb
    return f"""<expression label="{nom}" exp="{exp}" type="point"/>
<element type="point" label="{nom}">
	<show object="true" label="true"/>
	<objColor r="{r}" g="{g}" b="{b}" alpha="0"/>
	<layer val="0"/>
	<labelMode val="0"/>
	<fixed val="true"/>
	<pointSize val="{taille}"/>
	<pointStyle val="0"/>
</element>
"""

construction = (
    curseur("a", -0.5, -3, 3, 0.1, 40)
    + curseur("x_1", 1, -5, 10, 0.5, 100)
    + curseur("x_2", 7, -5, 10, 0.5, 160)
    + curseur("c", 0, -5, 5, 0.5, 220, visible=False)
    + fonction("f", "f(x) = a * (x - x_1) * (x - x_2)", (21, 101, 192))
    + texte("texte1", "&quot;Forme factorisée : f(x) = a (x − x₁) (x − x₂)&quot;", 250)
    + texte("texte2", "FormulaText(f, true, true)", 300, rgb=(21, 101, 192), latex=True)
    + point("R_1", "(x_1, 0)", (211, 47, 47))
    + point("R_2", "(x_2, 0)", (211, 47, 47))
    + """<expression label="T" exp="{(1, 0), (2, 2.5), (3, 4), (4, 4.5), (5, 4), (6, 2.5), (7, 0)}" type="list"/>
<element type="list" label="T">
	<show object="true" label="false"/>
	<objColor r="230" g="120" b="0" alpha="0"/>
	<layer val="0"/>
	<labelMode val="0"/>
	<fixed val="true"/>
	<pointSize val="5"/>
	<pointStyle val="0"/>
</element>
"""
    + fonction("g", "g(x) = a * x^(2) - a * (x_1 + x_2) * x + a * x_1 * x_2", (0, 0, 0), visible=False)
    + fonction("h", "h(x) = a * x^(2) + c", (0, 140, 70), visible=False)
)

xml = f"""<?xml version="1.0" encoding="utf-8"?>
<geogebra format="5.0" version="5.4.920.0" app="classic" platform="offline" xsi:noNamespaceSchemaLocation="https://www.geogebra.org/apps/xsd/ggb.xsd" xmlns="" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<gui>
	<font size="20"/>
</gui>
<euclidianView>
	<viewNumber viewNo="1"/>
	<size width="1100" height="650"/>
	<coordSystem xZero="330" yZero="500" scale="70" yscale="70"/>
	<evSettings axes="true" grid="true" gridIsBold="false" pointCapturing="3" rightAngleStyle="1" checkboxSize="26" gridType="3"/>
	<bgColor r="255" g="255" b="255"/>
	<axesColor r="28" g="28" b="31"/>
	<gridColor r="200" g="200" b="200"/>
	<lineStyle axes="1" grid="0"/>
	<axis id="0" show="true" label="" unitLabel="" tickStyle="1" showNumbers="true"/>
	<axis id="1" show="true" label="" unitLabel="" tickStyle="1" showNumbers="true"/>
</euclidianView>
<kernel>
	<continuous val="false"/>
	<usePathAndRegionParameters val="true"/>
	<decimals val="2"/>
	<angleUnit val="degree"/>
	<algebraStyle val="0" spreadsheet="0"/>
	<coordStyle val="0"/>
</kernel>
<construction title="Parabole - forme factorisée" author="A. Fernandez" date="">
{construction}</construction>
</geogebra>
"""

with zipfile.ZipFile("1ST2S_Ch5_Parabole.ggb", "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("geogebra.xml", xml)
print("1ST2S_Ch5_Parabole.ggb écrit")
