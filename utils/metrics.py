from prometheus_client import CollectorRegistry, Counter, Gauge, generate_latest
import prometheus_client

registry = CollectorRegistry()

tokenzer_reply = Gauge("usver_tokenzer_reply_time", "Время ответа от Tokenzer",registry=registry)
checked_tokens = Counter("usver_checked_tokens", "Количество проверенных токенов",registry=registry)

advents_profile= Counter("usver_advents_profile", "Количество получений профиля",registry=registry)
advents_time = Gauge("usver_advents_time", "Время получения профиля пользователя",registry=registry)

logins_sum = Counter("usver_logins_users", "Количество вошедших пользователей",registry=registry)
login_time = Gauge("usver_login_time", "Время входа пользователя",registry=registry)

sum_users = Counter("usver_sum_users", "Количество созданных пользователей",registry=registry)
registration_time = Gauge("usver_user_registration_time", "Время создания пользователя",registry=registry)

completed_verification = Counter("usver_sum_completed_verification", "Количество подтверждённых действий",registry=registry)
verification_time = Gauge("usver_verification_time", "Время подтверждения действия",registry=registry)

password_resets = Counter("usver_sum_password_resets", "Количество сбросов пароля",registry=registry)
reset_time = Gauge("usver_password_reset_time", "Время сброса пароля",registry=registry)

changes_profile = Counter("usver_sum_changes_profile", "Количество обновлений профиля",registry=registry)
change_time = Gauge("usver_profile_changes_time", "Время обновления профиля пользователя",registry=registry)