"""[Docstring del módulo: una sola línea que diga qué hace el programa.]"""

from typing import Final

# Añadid aquí las importaciones que necesitéis.

# ---------------------------------------------------------------------------
# Datos de la aplicación. Sustituid los del ejemplo APP-00 por los vuestros.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-00"
NOMBRE: Final[str] = "Agenda Escolar"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [1_200, 1_350, 1_280, 1_500, 0, 1_720,
                    2_050, 1_810, 1_980, 2_310, 2_200, 2_150]
CAIDAS: Final = [14, 12, 15, 9, 0, 22,
                 31, 8, 6, 9, 5, 4]

# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "[Iker Alcolea Mateos] · [David Raúl Rus Almajan]"
PENDIENTE: Final[str] = "  (opción pendiente de implementar)"

# ---------------------------------------------------------------------------
# Constantes comunes.
# ---------------------------------------------------------------------------
ANCHO: Final[int] = 44
POR_MIL: Final[int] = 1_000
UMBRAL_ESTABLE: Final[float] = 5.0       # caídas por cada mil descargas
UMBRAL_ACEPTABLE: Final[float] = 10.0
UMBRAL_REVISAR: Final[float] = 15.0
OPCION_SALIR: Final[int] = 9

# ---------------------------------------------------------------------------
# Constantes de la pareja. Todo valor fijo del programa va aquí, con nombre.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Funciones auxiliares. tasa_caidas viene hecha; el resto, con su docstring,
# las completáis vosotros. No cambiéis sus cabeceras.
# ---------------------------------------------------------------------------
def tasa_caidas(descargas: int, caidas: int) -> float:
    """Devuelve las caídas por cada mil descargas.

    Lanza ZeroDivisionError si la semana no tiene descargas.
    """
    return caidas / descargas * POR_MIL


def estado(descargas: int, caidas: int) -> str:
    """Devuelve el estado de una semana según su tasa de caídas.

    Es uno de estos textos: "Estable", "Aceptable", "Revisar", "Crítica" o
    "Mantenimiento", este último si la semana no tiene descargas.
    """
    if descargas == 0:
        return "MAntenimiento"

    tasa = (caidas / descargas) * 1000

    if tasa < 50:
        return "EStable"
    if tasa < 100:
        return "Aceptable"
    if tasa < 150:
        return "Revisar"
    else:
        return "Critica"


def pedir_entero(mensaje: str, minimo: int, maximo: int) -> int:
    """Pide un entero entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un entero o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: El valor debe estar entre el minimo y el máximo: {minimo}-{maximo}")
        except ValueError:
            print("Error, número inválido")
    return minimo                     # provisional


def pedir_real(mensaje: str, minimo: float, maximo: float) -> float:
    """Pide un número real entre minimo y maximo hasta que sea válido.

    Si se escribe algo que no es un número o está fuera de rango, avisa y
    lo vuelve a pedir.
    """
    while True:
        try:
            valor = float(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Error: debe estar entre el mínimo y el máximo: {minimo}-{maximo}")
        except ValueError:
            print("Error, número inválido")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """
    try:
        semana = int(texto)
        if 1 <= semana <= len(DESCARGAS):
            return semana
        raise ValueError("SEmana fuera de rango")
    except ValueError:
        raise ValueError("Semana no válida")


def comprobar_datos() -> int:
    """Revisa los datos semanales y devuelve el número de errores.

    Registra cada error con logging.error y cada semana de mantenimiento
    con logging.warning.
    """
    return 0                          # provisional


# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """[Docstring: qué hace esta función.]"""
    print(PENDIENTE)


def opcion_1_listado() -> None:
    """Muestra las descargas, las caídas y la tasa de cada semana."""
    print(f"{'Semana':>6}{'Descargas':>11}{'Caídas':>8}{'Tasa ‰':>9}")
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        try:
            tasa = f"{tasa_caidas(descargas, caidas):.1f}"
        except ZeroDivisionError:
            tasa = "—"
        print(f"{semana:>6}{descargas:>11}{caidas:>8}{tasa:>9}")


def opcion_2_resumen() -> None:
    """Muestra los totales, la media y las semanas extremas."""
    total_descargas = 0
    total_caidas = 0
    activas = 0
    mas = 0
    semana_mas = 0
    menos = None
    semana_menos = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue
        activas += 1
        total_descargas += descargas
        total_caidas += caidas
        if descargas > mas:
            mas = descargas
            semana_mas = semana
        if menos is None or descargas < menos:
            menos = descargas
            semana_menos = semana
    media = total_descargas / activas
    tasa = tasa_caidas(total_descargas, total_caidas)
    print(f"Semanas activas:     {activas} de {len(DESCARGAS)}")
    print(f"Total de descargas:  {total_descargas}")
    print(f"Media semanal:       {media:.1f}")
    print(f"Más descargas:       semana {semana_mas} ({mas})")
    print(f"Menos descargas:     semana {semana_menos} ({menos})")
    print(f"Total de caídas:     {total_caidas}")
    print(f"Tasa global:         {tasa:.1f} ‰")


def opcion_3_estabilidad() -> None:
    """[Docstring: Obtiene el estado de estabilidad cada semana y su recuento.]"""
    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            mantenimiento += 1
            print(f"Semana {semana}: Mantenimiento")
            continue
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana}: {estado_semana}")

        match estado_semana:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica": 
                criticas += 1
    print(f"Semanas estables:{estables}")
    print(f"Semanas aceptables:{aceptables}")
    print(f"Semanas a revisar: {revisar}")
    print(f"Semanas críticas: {criticas}")       
    print(f"Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """[Docstring: Muestra la primera semana que alcanzaz o supera el umbral por mil.]"""
    umbral = pedir_real("Umbral de caídas por mil: ", 0, 1000)

    for semana,(descargas, caidas) in enumerate(
        zip(DESCARGAS, CAIDAS), start=1):
        if descargas == 0:
            continue

        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera Semana {semana}: {tasa:.1f} ‰")
            break
        else:
            print(f"Ninguna semana alcanza el umbral de {umbral:.1f} ‰")


def opcion_5_racha() -> None:
    """[Muestra la racha más larga de semanas seguidas con el estado Estable o aceptable.]"""
    mejor_racha = 0
    inicio_mejor = 0
    racha_actual = 0
    inicio_actual = 0

    for semana,(descargas, caidas) in enumerate(
        zip(DESCARGAS, CAIDAS), start=1
    ):
        if descargas == 0:
            continue

        estado_caidas = estado(descargas, caidas)

    if estado_caidas in ("Estable", "Aceptable"):
        if racha_actual == 0:
            inicio_actual = semana
        racha_actual +=1

        if racha_actual > mejor_racha:
            mejor_racha = racha_actual
            inicio_mejor = inicio_actual
        else:
            racha_actual = 0
            inicio_actual = 0
    if mejor_racha > 0:
        print(f"Mejor racha: {mejor_racha}, semana de inicio: {inicio_mejor}")
    else:
        print("NO hay racha")



def opcion_6_prevision() -> None:
    """[Docstring: qué hace esta opción.]"""
    print(PENDIENTE)


def opcion_7_consulta() -> None:
    """[Docstring: qué hace esta opción.]"""
    print(PENDIENTE)


def opcion_8_comprobar() -> None:
    """[Docstring: qué hace esta opción.]"""
    print(PENDIENTE)


def main() -> None:
    """[Docstring: qué hace la función principal.]"""
    # Provisional: sustituidlo por el bucle del menú (tarea 2).
    mostrar_menu()
    opcion_1_listado()
    opcion_2_resumen()
    print(PENDIENTE)


if __name__ == "__main__":
    main()
