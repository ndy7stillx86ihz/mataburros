### Definición de los modelos de acuerdo a los tipos de relaciones

**One to many**

* Clase Padre: 
Declaración de la relación, como contenedor de varios elementos de la hija.

```
children : Mapped[List["children"]] = relationship(back_populates="parent")
```
``
* Clase Hijo:
Declarar una ForeignKey y la relación con la clase padre.

```
parent: Mapped["Parent"] = relationship(back_populates="children")
```

**Many to One**

* Clase Padre:

```
child: Mapped ["Child"] = relationship(back_populates="parent")
```

* Clase Hijo:

```
parent : Mapped[List["Parent"]] = relationship(back_populates="child")
```

**Nullable Many to One**

* Clase Padre:

```
child: Mapped[Optional["Child"]] = relationship(back_populates="parent")
```

* Clase Hija:
```
parent: Mapped[List["Parent"]] = relationship(back_populates="child")
```

**One to One**
* Clase Padre:
```
child: Mapped["Child"] = relationship(back_populates="parent")
```

* Clase Hijo:

```
parent: Mapped["Parent"] = relationship(back_populates= "child")
```

**Many to Many**

* Tabla de asociación:
```
from sqlalchemy import Table 

name_table_associaton = Table(
	"name_table_associaton",
		Base.metadata,
Column("name_first_table_id", ForeignKey("name_first_table.id"), primary_key=True),
Column("name_second_table_id", ForeignKey("name_second_table.id"), primary_key=True) 
)
```

* First table
```
relation_1: Mapped[List[Class2]] = relationship(secondary=name_table_associaton, back_populates="relation2")
```

* Second table
```
relation2: Mapped[List[Class1]] = relationship(secondary=name_table_associaton, backpopulates= "relation_1")
```

*Aclaración*: La declaración primary_key = True define que las combinaciones de los dos valores debe ser única para generar una primary key para la tabla asociativa. Evita duplicados.




