# Crontab

En Windows, el 'crontab' se llama 'Programador de Tareas' o en ingles 'Task Scheduler'.
Se pueden realizar todas las configuraciones desde la aplicacion grafica o bien desde la linea de comandos.

Aqui mostrare hacerlo desde la linea de comandos.

## Task Scheduler Cheet Sheet

* buscar el exe (ejecutable) a programar, en mi caso *sanfi*
```cmd
where sanfi
C:\Users\Oscar\AppData\Roaming\Python\Python310\Scripts\sanfi.exe
```

* crear la tarea (todos los dias a las 08:00), una para la cuenta y otra para la tarjeta Visa
```cmd
schtasks /create /tn sanfi_debit /tr "C:\Users\Oscar\AppData\Roaming\Python\Python310\Scripts\sanfi.exe --download --debit" /sc daily /st 08:00
schtasks /create /tn sanfi_visa /tr "C:\Users\Oscar\AppData\Roaming\Python\Python310\Scripts\sanfi.exe --download --visa" /sc daily /st 08:15
```

* mostrar las tareas
```cmd
schtasks /Query /TN \sanfi_debit /fo list /v
schtasks /Query /TN \sanfi_visa /fo list /v
```

* ejecutar manualmente la tarea
```cmd
schtasks /RUN /TN sanfi_debit
schtasks /RUN /TN sanfi_visa
```

* borrar una tarea
```cmd
schtasks /Delete /TN sanfi_debit /F
schtasks /Delete /TN sanfi_visa /F
```
