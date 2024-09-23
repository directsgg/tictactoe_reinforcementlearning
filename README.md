# Totito con Aprendizaje por Refuerzo

Este proyecto es un juego de Totito implementado en Python utilizando Pygame para la interfaz gráfica y aprendizaje por refuerzo para la lógica del juego.

## Descripción

El juego de Totito (o tres en raya) es un juego de mesa clásico en el que dos jugadores se turnan para marcar espacios en una cuadrícula de 3x3. El objetivo es conseguir tres de tus símbolos en una fila, columna o diagonal antes que tu oponente.

En esta implementación, uno o ambos jugadores pueden ser agentes controlados por computadora que utilizan aprendizaje por refuerzo para mejorar su estrategia de juego.

## Requisitos

- Python 3.7.9
- Pygame
- Numpy

Puedes instalar las dependencias necesarias ejecutando:

```bash
pip install pygame numpy
```


## Uso
Para ejecutar el juego, simplemente corre el archivo principal del proyecto:
```bash
python totes.py
```

## Estructura del Código
State: Clase que representa el estado del juego, maneja la lógica del juego y dibuja el tablero.
Agent: Clase que representa un agente que utiliza aprendizaje por refuerzo para jugar.

totes.py: Archivo principal que inicializa el juego y controla el flujo del programa.

## Funcionalidades
Interfaz Gráfica: Utiliza Pygame para dibujar el tablero y los símbolos de los jugadores.

Aprendizaje por Refuerzo: Los agentes pueden aprender y mejorar su estrategia de juego a través de la experiencia.

Modo de Juego: Permite jugar contra otro jugador humano o contra un agente controlado por computadora.