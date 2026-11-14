from django.test import SimpleTestCase
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Task
from .serializers import TaskSerializer


class TaskSerializerTests(SimpleTestCase):
    def test_accepts_valid_task_with_aziz_title(self):
        serializer = TaskSerializer(
            data={
                "title": "Азиз",
                "description": "Описание задачи",
                "priority": 1,
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_rejects_empty_or_whitespace_title(self):
        for title in ("", "   "):
            with self.subTest(title=title):
                serializer = TaskSerializer(
                    data={
                        "title": title,
                        "description": "Описание задачи",
                        "priority": 3,
                    }
                )

                self.assertFalse(serializer.is_valid())
                self.assertIn("title", serializer.errors)

    def test_rejects_description_shorter_than_ten_characters(self):
        serializer = TaskSerializer(
            data={"title": "Азиз", "description": "Коротко", "priority": 3}
        )

        self.assertFalse(serializer.is_valid())
        self.assertIn("description", serializer.errors)

    def test_rejects_priority_outside_one_to_five(self):
        for priority in (0, 6):
            with self.subTest(priority=priority):
                serializer = TaskSerializer(
                    data={
                        "title": "Азиз",
                        "description": "Описание задачи",
                        "priority": priority,
                    }
                )

                self.assertFalse(serializer.is_valid())
                self.assertIn("priority", serializer.errors)


class TaskAPITests(APITestCase):
    list_url = "/api/tasks/"

    def valid_payload(self, **overrides):
        payload = {
            "title": "Подготовить отчет",
            "description": "Собрать и проверить данные",
            "priority": 3,
        }
        payload.update(overrides)
        return payload

    def test_list_tasks(self):
        Task.objects.create(
            title="Подготовить отчет",
            description="Собрать и проверить данные",
            priority=3,
        )

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_task(self):
        response = self.client.post(
            self.list_url, self.valid_payload(), format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(response.data["priority"], 3)
        self.assertIn("created_at", response.data)

    def test_create_task_rejects_invalid_fields(self):
        invalid_payloads = (
            self.valid_payload(title="   "),
            self.valid_payload(description="Коротко"),
            self.valid_payload(priority=0),
            self.valid_payload(priority=6),
        )

        for payload in invalid_payloads:
            with self.subTest(payload=payload):
                response = self.client.post(self.list_url, payload, format="json")
                self.assertEqual(
                    response.status_code, status.HTTP_400_BAD_REQUEST
                )

    def test_retrieve_and_delete_task(self):
        task = Task.objects.create(
            title="Подготовить отчет",
            description="Собрать и проверить данные",
            priority=3,
        )
        detail_url = f"{self.list_url}{task.pk}/"

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], task.pk)

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())
