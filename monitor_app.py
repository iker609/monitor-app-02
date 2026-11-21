"""Monitor de estabilidad semanal de aplicaciones móviles."""

import logging
import sys
from typing import Final

# ---------------------------------------------------------------------------
# Datos de la aplicación.
# ---------------------------------------------------------------------------
CODIGO: Final[str] = "APP-02"
NOMBRE: Final[str] = "Lista de la Compra"
# Una posición por semana, de la 1 a la 12. 0 descargas: app retirada.
DESCARGAS: Final = [2_750, 2_850, 3_160, 3_450, 3_660, 4_060,
                    4_190, 4_270, 0, 4_260, 4_520, 4_450]
CAIDAS: Final = [44, 14, 45, 32, 17, 26,
                 14, 13, 0, 37, 104, 11]

# ---------------------------------------------------------------------------
# Datos del programa. Solo hay que cambiar AUTORES.
# ---------------------------------------------------------------------------
VERSION_PROGRAMA: Final[str] = "1.0.0"
AUTORES: Final[str] = "Iker Alcolea Mateos · David Raúl Rus Almaján"
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
PRIMERA_OPCION: Final[int] = 1
PRIMERA_SEMANA: Final[int] = 1
UMBRAL_MIN: Final[float] = 0.0
UMBRAL_MAX: Final[float] = 1_000.0
OBJETIVO_MAX: Final[int] = 1_000_000
CRECIMIENTO_MIN: Final[float] = 0.5
CRECIMIENTO_MAX: Final[float] = 50.0
CIEN_POR_CIEN: Final[float] = 100.0
MAX_SEMANAS_PREVISION: Final[int] = 104
RESPUESTAS_SALIR: Final[tuple[str, str]] = ("s", "S")


# ---------------------------------------------------------------------------
# Excepciones propias de la pareja. Aquí va SemanaNoValida (opción 7).
# ---------------------------------------------------------------------------
class SemanaNoValida(Exception):
    """Excepción lanzada cuando el número de semana no es válido."""


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
        return "Mantenimiento"

    tasa = tasa_caidas(descargas, caidas)
    if tasa < UMBRAL_ESTABLE:
        return "Estable"
    if tasa < UMBRAL_ACEPTABLE:
        return "Aceptable"
    if tasa < UMBRAL_REVISAR:
        return "Revisar"
    return "Crítica"


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
            print(f"  El valor debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("  Introduce un número entero válido.")


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
            print(f"  El valor debe estar entre {minimo} y {maximo}.")
        except ValueError:
            print("  Introduce un número válido.")


def semana_valida(texto: str) -> int:
    """Convierte el texto en un número de semana de los datos.

    Lanza SemanaNoValida si no es un entero o está fuera de rango.
    """
    try:
        semana = int(texto)
    except ValueError:
        raise SemanaNoValida(f"«{texto}» no es un número de semana") from None

    total_semanas = len(DESCARGAS)
    if not (PRIMERA_SEMANA <= semana <= total_semanas):
        raise SemanaNoValida(
            f"la semana {semana} no existe: "
            f"hay de {PRIMERA_SEMANA} a {total_semanas}"
        )
    return semana


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
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
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
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
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
    """Muestra el estado de estabilidad de cada semana y el recuento."""
    estables = 0
    aceptables = 0
    revisar = 0
    criticas = 0
    mantenimiento = 0
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
        estado_semana = estado(descargas, caidas)
        print(f"Semana {semana:>2}: {estado_semana}")
        match estado_semana:
            case "Estable":
                estables += 1
            case "Aceptable":
                aceptables += 1
            case "Revisar":
                revisar += 1
            case "Crítica":
                criticas += 1
            case "Mantenimiento":
                mantenimiento += 1
    print("-" * ANCHO)
    print(
        f"Estables: {estables} · Aceptables: {aceptables} · "
        f"Revisar: {revisar}"
    )
    print(f"Críticas: {criticas} · Mantenimiento: {mantenimiento}")


def opcion_4_umbral() -> None:
    """Muestra la primera semana que alcanza o supera un umbral por mil."""
    umbral = pedir_real("Umbral en caídas por mil: ", UMBRAL_MIN, UMBRAL_MAX)
    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
        if descargas == 0:
            continue
        tasa = tasa_caidas(descargas, caidas)
        if tasa >= umbral:
            print(f"Primera semana: {semana} ({tasa:.1f} ‰)")
            break
    else:
        print(f"Ninguna semana alcanza {umbral:.1f} ‰")


def opcion_5_racha() -> None:
    """Muestra la racha más larga de semanas seguidas sin problemas."""
    mejor_racha = 0
    inicio_mejor = 0
    racha_actual = 0
    inicio_actual = 0

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
        if descargas == 0:
            continue

        estado_semana = estado(descargas, caidas)
        if estado_semana in ("Estable", "Aceptable"):
            if racha_actual == 0:
                inicio_actual = semana
            racha_actual += 1
            if racha_actual > mejor_racha:
                mejor_racha = racha_actual
                inicio_mejor = inicio_actual
        else:
            racha_actual = 0
            inicio_actual = 0

    if mejor_racha > 0:
        print(
            f"Mejor racha: {mejor_racha} semanas, "
            f"desde la semana {inicio_mejor}"
        )
    else:
        print("No hay ninguna racha sin problemas")


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
