# pystats
My ascii visualizations. At the moment, it includes  [Scott-Knott tests](https://github.com/timm/sbse14/wiki/skpy) and a simple histogram plot in ascii.

## Output of SK tests
```
rank ,         name ,    med   ,  iqr 
----------------------------------------------------
   1 ,           x1 ,    1100  ,     0 (*              |              ),11.00, 11.00, 11.00, 11.00, 11.00
   1 ,           x2 ,    1100  ,     0 (*              |              ),11.00, 11.00, 11.00, 11.00, 11.00
   2 ,           x4 ,    3400  ,   200 (               |          - * ),32.00, 33.00, 34.00, 34.00, 35.00
```

## Histogram

```
Name,      Range,                                Value
-------------------------------------------------------
After      2 - 3  |*****************           | 75%
After      2 - 3  |********************        | 75%
Before     0 - 1  |***********************     | 97%
Before     0 - 1  |*************************   | 97%
Before     0 - 1  |********************        | 97%
After      2 - 3  |*****************           | 75%

```
