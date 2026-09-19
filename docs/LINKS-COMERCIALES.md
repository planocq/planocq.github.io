# Links únicos de PLANO:CQ

Todo nuevo `/1/x/` se crea exclusivamente con `tools/unique_link.py`. No editar HTML ni generar rutas por otro método.

## Operación Comercial

Desde la raíz de este repositorio (o la copia local `PLANO-CQ GitHub`), con Python 3.9+ y GitHub CLI autenticado como `planocq`:

```sh
python3 tools/unique_link.py create
```

No requiere datos personales ni ID: asigna el siguiente número libre y devuelve JSON con `id`, `url` y `commit`. Se puede solicitar un ID libre con `--id NUMERO`; nunca sobrescribe existentes. Esperar `status: VERIFICADO` antes de usar la URL. Si la publicación tarda o se interrumpe después de devolver un ID, **no repetir create**:

```sh
python3 tools/unique_link.py verify NUMERO --wait 180
```

Comercial conserva la URL devuelta para su destinatario; este comando no consulta ni modifica CRM y no envía mensajes. Si el proceso no puede ejecutar comandos, debe solicitar la ejecución de este comando exacto a Codex; no reconstruir páginas con el conector.

## Implementación única

El generador toma la metadata aprobada del `index.html` remoto en el mismo commit base. Produce Open Graph/Twitter estáticos, imagen HTTPS, noindex y `og:url`/canonical propios. Carga `/` con el mismo mecanismo validado en revisión interna, conserva la URL del navegador y el beacon Cloudflare de la home; mantiene la identidad propia también tras ejecutar JavaScript. El tracking individual corresponde a la ruta de entrada; no añade seguimiento individual a páginas posteriores.

Asigna ID según rutas remotas existentes, publica sólo una página y actualiza `main` sin force; una colisión concurrente falla sin sobrescribir. La publicación mediante credencial de usuario dispara GitHub Pages. Verifica HTTP 200 sin redirect, metadata sin JS, identidad y disponibilidad de imagen; la comprobación de Apple Mail sigue siendo manual. Para pruebas usar `create --test`; el ID queda reservado como prueba en el commit y no se asigna a contactos.

La metadata común se mantiene en la home y se incorpora al generar cada link. Cambiarla no migra retroactivamente links existentes: esa actualización necesita una tarea explícita. El workflow antiguo de generación masiva fue sustituido por tests sin escritura. Las rutas históricas 1–50 permanecen sin migrar en esta etapa; `/1/51/` es la única prueba nueva y queda reservada.
