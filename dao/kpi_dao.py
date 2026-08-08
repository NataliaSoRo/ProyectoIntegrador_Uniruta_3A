from database.conexion import Conexion


class KpiDAO:
    def obtener_resumen_kpis(self):
        conexion = Conexion.obtener_conexion()
        datos = {
            "unidades_activas": 0,
            "total_unidades": 0,
            "choferes_en_turno": 0,
            "total_choferes": 0,
            "viajes_programados": 0,
            "viajes_completados": 0,
            "ganancias_totales": 0.0,
        }
        if conexion is None:
            return datos

        try:
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM unidad WHERE estatus = 'Activo';")
                    datos["unidades_activas"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM unidad;")
                    datos["total_unidades"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'unidad':", e)

            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM choferes WHERE estatus = 'Activo';")
                    datos["choferes_en_turno"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM choferes;")
                    datos["total_choferes"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'choferes':", e)

            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM viaje WHERE estatus = 'Programado';")
                    datos["viajes_programados"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM viaje WHERE estatus IN ('Finalizado', 'Completado');")
                    datos["viajes_completados"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'viaje':", e)

            # Ganancias generales: suma de (pasajeros * tarifa) de cada viaje
            try:
                with conexion.cursor() as cursor:
                    sql_ganancias = """
                        SELECT COALESCE(SUM(v.pasajeros::numeric * r.tarifa), 0)
                        FROM viaje v
                        JOIN ruta r ON v.id_ruta = r.id
                        WHERE v.pasajeros IS NOT NULL
                          AND v.pasajeros::text ~ '^[0-9]+$'
                          AND r.tarifa IS NOT NULL;
                    """
                    cursor.execute(sql_ganancias)
                    resultado = cursor.fetchone()[0]
                    datos["ganancias_totales"] = float(resultado) if resultado else 0.0
            except Exception as e:
                conexion.rollback()
                print("Aviso calculando ganancias:", e)

        except Exception as ex:
            print("Aviso general en KpiDAO:", ex)
        finally:
            conexion.close()

        return datos

    def obtener_ganancias_por_ruta(self):
        """Devuelve lista de tuplas (nombre_ruta, ganancia_total),
        donde ganancia_total = suma de (pasajeros * tarifa) de todos
        los viajes de esa ruta."""
        conexion = Conexion.obtener_conexion()
        resultados = []
        if conexion is None:
            return resultados

        try:
            with conexion.cursor() as cursor:
                sql = """
                    SELECT r.nombre AS ruta, COALESCE(SUM(v.pasajeros::numeric * r.tarifa), 0) AS ganancia
                    FROM viaje v
                    JOIN ruta r ON v.id_ruta = r.id
                    WHERE v.pasajeros IS NOT NULL
                      AND v.pasajeros::text ~ '^[0-9]+$'
                      AND r.tarifa IS NOT NULL
                    GROUP BY r.nombre
                    ORDER BY ganancia DESC;
                """
                cursor.execute(sql)
                resultados = cursor.fetchall()
        except Exception as e:
            conexion.rollback()
            print("Aviso obteniendo ganancias por ruta:", e)
        finally:
            conexion.close()

        return resultados

    def obtener_prioridades(self):
        conexion = Conexion.obtener_conexion()
        lista_prioridades = []

        if conexion is None:
            return lista_prioridades

        try:
            try:
                with conexion.cursor() as cursor:
                    sql_choferes = """
                        SELECT 
                            'Licencia por vencer/vencida' AS tipo,
                            nombre AS entidad,
                            estatus AS estado
                        FROM choferes 
                        WHERE vigen_licencia <= CURRENT_DATE + INTERVAL '30 days'
                           OR estatus = 'Vencido';
                    """
                    cursor.execute(sql_choferes)
                    lista_prioridades.extend(cursor.fetchall())
            except Exception as e:
                conexion.rollback()
                print("Aviso prioridades choferes:", e)

            try:
                with conexion.cursor() as cursor:
                    sql_unidad = """
                        SELECT 
                            'Unidad fuera de servicio' AS tipo,
                            CONCAT("No_economico", ' (', placas, ')') AS entidad,
                            estatus AS estado
                        FROM unidad 
                        WHERE estatus IN ('Mantenimiento', 'Baja', 'Inactivo');
                    """
                    cursor.execute(sql_unidad)
                    lista_prioridades.extend(cursor.fetchall())
            except Exception as e:
                conexion.rollback()
                print("Aviso prioridades unidad:", e)

            try:
                with conexion.cursor() as cursor:
                    sql_viaje = """
                        SELECT 
                            'Viaje sin asignación' AS tipo,
                            CONCAT('Viaje #', id, ' (', origen, ' -> ', destino, ')') AS entidad,
                            estatus AS estado
                        FROM viaje 
                        WHERE id_chofer IS NULL OR id_unidad IS NULL;
                    """
                    cursor.execute(sql_viaje)
                    lista_prioridades.extend(cursor.fetchall())
            except Exception as e:
                conexion.rollback()
                print("Aviso prioridades viaje:", e)

        except Exception as ex:
            print("Aviso al consultar prioridades dinámicas:", ex)
        finally:
            conexion.close()

        return lista_prioridades[:5]