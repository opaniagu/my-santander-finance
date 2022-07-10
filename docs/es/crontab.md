# Crontab

En Windows, el 'crontab' se llama 'Programador de Tareas' o en ingles 'Task Scheduler'.
Se pueden realizar todas las configuraciones desde la aplicacion grafica o bien desde la linea de comandos.

Aqui mostrare hacerlo desde la linea de comandos.

## Task Scheduler Cheet Sheet

* buscar el exe (ejecutable) a programar
```cmd
where sanfi
C:\Users\Oscar\AppData\Roaming\Python\Python310\Scripts\sanfi.exe
```

* crear la tarea (todos los dias a las 08:00)
```cmd
schtasks /create /tn sanfi /tr "C:\Users\Oscar\AppData\Roaming\Python\Python310\Scripts\sanfi.exe --download" /sc daily /st 08:00
```

* mostrar la tarea
```cmd
schtasks /Query /TN \sanfi /fo list /v
```

* ejecutar manualmente la tarea
```cmd
schtasks /RUN /TN sanfi
```

* borrar una tarea
```cmd
schtasks /Delete /TN sanfi /F
```
