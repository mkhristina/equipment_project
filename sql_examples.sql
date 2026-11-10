
-- ЗАПРОС 1. Заявки на обслуживание по приоритету
SELECT
    r.id,
    e.inventory_number,
    e.name AS equipment_name,
    r.description,
    r.priority,
    r.status
FROM maintenance_maintenancerequest r
JOIN maintenance_equipment e
    ON r.equipment_id = e.id
ORDER BY
    CASE r.priority
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END;


-- ЗАПРОС 2. Количество заявок по статусам
SELECT
    status,
    COUNT(*) AS requests_count
FROM maintenance_maintenancerequest
GROUP BY status
ORDER BY status;


-- ЗАПРОС 3. Оборудование без активных заявок
-- Активными считаются заявки со статусом new или in_progress
SELECT
    e.id,
    e.inventory_number,
    e.name
FROM maintenance_equipment e
WHERE NOT EXISTS (
    SELECT 1
    FROM maintenance_maintenancerequest r
    WHERE r.equipment_id = e.id
      AND r.status IN ('new', 'in_progress')
)
ORDER BY e.inventory_number;


-- ЗАПРОС 4. Самое проблемное оборудование
-- Считаем общее количество заявок для каждого оборудования
SELECT
    e.id,
    e.inventory_number,
    e.name,
    COUNT(r.id) AS requests_count
FROM maintenance_equipment e
LEFT JOIN maintenance_maintenancerequest r
    ON r.equipment_id = e.id
GROUP BY
    e.id,
    e.inventory_number,
    e.name
ORDER BY
    requests_count DESC,
    e.inventory_number;
