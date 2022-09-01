from pytest import MonkeyPatch

mp = MonkeyPatch()
mp.setenv("DB_URL", "sqlite://")
