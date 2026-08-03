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
            "viajes_completados": 0
        }
        if conexion is None:
            return datos

        try:
            # 1. Tabla 'unidad'
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM unidad WHERE estatus = 'Activo';")
                    datos["unidades_activas"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM unidad;")
                    datos["total_unidades"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'unidad':", e)

            # 2. Tabla 'choferes'
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM choferes WHERE estatus = 'Activo';")
                    datos["choferes_en_turno"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM choferes;")
                    datos["total_choferes"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'choferes':", e)

            # 3. Tabla 'viaje'
            try:
                with conexion.cursor() as cursor:
                    cursor.execute("SELECT COUNT(*) FROM viaje WHERE estatus = 'Programado';")
                    datos["viajes_programados"] = cursor.fetchone()[0] or 0
                    cursor.execute("SELECT COUNT(*) FROM viaje WHERE estatus IN ('Finalizado', 'Completado');")
                    datos["viajes_completados"] = cursor.fetchone()[0] or 0
            except Exception as e:
                conexion.rollback()
                print("Aviso leyendo 'viaje':", e)

        except Exception as ex:
            print("Aviso general en KpiDAO:", ex)
        finally:
            conexion.close()

        return datos

    def obtener_prioridades(self):
        conexion = Conexion.obtener_conexion()
        lista_prioridades = []
        
        if conexion is None:
            return lista_prioridades

        try:
            # 1. Alertas de Choferes
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

            # 2. Alertas de Unidades (usando comillas dobles para "No_economico")
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

            # 3. Alertas de Viajes
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