import pytest

def test_add_and_get_all_visits(visit_repository, clear_visit_logs):
    # Сначала база пуста
    visits = visit_repository.get_all_visits()
    assert visits == []

    # Добавим посещение
    visit_repository.add_visit(user_id=1, page='home')

    visits = visit_repository.get_all_visits()
    assert len(visits) == 1
    assert visits[0].user_id == 1
    assert visits[0].page == 'home'


def test_get_all_visits_with_example_visits(visit_repository, example_visits, clear_visit_logs):
    # example_visits уже добавлены в БД
    visits = visit_repository.get_all_visits()
    assert len(visits) == len(example_visits)
    # Проверим, что каждый визит из example_visits есть в репозитории
    for ev in example_visits:
        assert any(v.id == ev.id and v.user_id == ev.user_id and v.page == ev.page for v in visits)


def test_clear_visit_logs(visit_repository, example_visits, clear_visit_logs):
    visits_before = visit_repository.get_all_visits()
    assert len(visits_before) > 0

    # После очистки таблицы visits будет пусто
    visits_after = visit_repository.get_all_visits()
    assert visits_after == []
