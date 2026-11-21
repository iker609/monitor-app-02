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
    errores = 0
    if len(DESCARGAS) != len(CAIDAS):
        logging.error(
            "las listas no tienen la misma longitud (%d y %d)",
            len(DESCARGAS),
            len(CAIDAS),
        )
        errores += 1

    for semana, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
        if descargas < 0:
            logging.error(
                "semana %d: descargas negativas (%d)", semana, descargas
            )
            errores += 1
        if caidas < 0:
            logging.error("semana %d: caídas negativas (%d)", semana, caidas)
            errores += 1
        if descargas >= 0 and caidas > descargas:
            logging.error("semana %d: más caídas que descargas", semana)
            errores += 1
        elif descargas == 0:
            logging.warning(
                "semana %d: sin descargas (mantenimiento)", semana
            )

    return errores


# ---------------------------------------------------------------------------
# Menú y opciones. La opción 1 viene hecha y la 2 tiene dos errores.
# ---------------------------------------------------------------------------
def mostrar_menu() -> None:
    """Muestra la cabecera del monitor y las opciones disponibles."""
    linea = "=" * ANCHO
    titulo = f"MONITOR DE {CODIGO} · {NOMBRE}"
    print(linea)
    print(titulo.center(ANCHO))
    print(linea)
    print("1. Listado semanal")
    print("2. Resumen")
    print("3. Estabilidad por semana")
    print("4. Primera semana que alcanza un umbral")
    print("5. Mejor racha sin problemas")
    print("6. Previsión de crecimiento")
    print("7. Consultar una semana")
    print("8. Comprobar los datos")
    print("9. Salir")


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
    """Calcula en cuántas semanas se alcanza un objetivo de descargas."""
    ultima_activa = 0
    for descargas in DESCARGAS:
        if descargas > 0:
            ultima_activa = descargas

    print(f"Descargas de la última semana activa: {ultima_activa}")
    objetivo = pedir_entero(
        "Objetivo semanal de descargas: ", ultima_activa + 1, OBJETIVO_MAX
    )
    crecimiento = pedir_real(
        "Crecimiento semanal en %: ", CRECIMIENTO_MIN, CRECIMIENTO_MAX
    )
    factor = 1 + crecimiento / CIEN_POR_CIEN
    proyeccion = float(ultima_activa)
    semanas = 0

    while proyeccion < objetivo:
        if semanas >= MAX_SEMANAS_PREVISION:
            print(
                f"No se alcanza el objetivo en {MAX_SEMANAS_PREVISION} semanas"
            )
            break
        proyeccion *= factor
        semanas += 1
    else:
        descargas_finales = round(proyeccion)
        print(
            f"Se alcanza en {semanas} semanas "
            f"({descargas_finales} descargas)"
        )


def opcion_7_consulta() -> None:
    """Muestra los datos, el estado y la acción recomendada de una semana."""
    total_semanas = len(DESCARGAS)
    texto = input(f"Semana ({PRIMERA_SEMANA}-{total_semanas}): ")
    try:
        semana = semana_valida(texto)
    except SemanaNoValida as error:
        print(f"  No se puede consultar: {error}")
        return

    for num, (descargas, caidas) in enumerate(
            zip(DESCARGAS, CAIDAS), start=PRIMERA_SEMANA):
        if num == semana:
            estado_semana = estado(descargas, caidas)
            match estado_semana:
                case "Estable":
                    accion = "Sin acciones"
                case "Aceptable":
                    accion = "Vigilar en la próxima versión"
                case "Revisar":
                    accion = "Revisar los informes de errores"
                case "Crítica":
                    accion = "Publicar una versión correctora urgente"
                case "Mantenimiento":
                    accion = "La app no estuvo publicada esa semana"
            print(f"Descargas: {descargas}")
            print(f"Caídas:    {caidas}")
            print(f"Estado:    {estado_semana}")
            print(f"Acción:    {accion}")
            break


def opcion_8_comprobar() -> None:
    """Comprueba los datos semanales y muestra el resultado."""
    errores = comprobar_datos()
    if errores == 0:
        print(f"Datos correctos: {len(DESCARGAS)} semanas")
    else:
        print("Los datos tienen errores: corrígelos antes de continuar.")


def main() -> None:
    """Punto de entrada principal con validación inicial y bucle del menú."""
    logging.basicConfig(
        level=logging.WARNING, format="%(levelname)s: %(message)s"
    )
    try:
        if comprobar_datos() > 0:
            sys.exit("Los datos tienen errores: corrígelos antes de continuar.")

        print(f"Monitor de estabilidad {VERSION_PROGRAMA} · {AUTORES}")
        while True:
            mostrar_menu()
            entrada = input("Opción: ")
            try:
                opcion = int(entrada)
            except ValueError:
                print(f"  «{entrada}» no es una opción.")
                continue

            match opcion:
                case 1:
                    opcion_1_listado()
                case 2:
                    opcion_2_resumen()
                case 3:
                    opcion_3_estabilidad()
                case 4:
                    opcion_4_umbral()
                case 5:
                    opcion_5_racha()
                case 6:
                    opcion_6_prevision()
                case 7:
                    opcion_7_consulta()
                case 8:
                    opcion_8_comprobar()
                case _ if opcion == OPCION_SALIR:
                    confirmar = input("¿Salir del programa? (s/n): ")
                    if confirmar in RESPUESTAS_SALIR:
                        break
                case _:
                    print(
                        f"  Elige una opción entre {PRIMERA_OPCION} "
                        f"y {OPCION_SALIR}."
                    )
    except KeyboardInterrupt:
        print("\nPrograma interrumpido.")

    print(f"Fin del monitor de {CODIGO}.")


if __name__ == "__main__":
    main()
