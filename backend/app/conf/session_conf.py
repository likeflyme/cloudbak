from pydantic import BaseModel


class AnalyzeConfig(BaseModel):
    analyze_open: bool = False
    analyze_cron: str = '0 1 * * *'


class SessionConfig(BaseModel):
    analyze: AnalyzeConfig = AnalyzeConfig()



