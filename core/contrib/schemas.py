from pydantic import BaseModel


class BaseSchemaMixin(BaseModel):
    class Config:
        extra = 'forbid'
        orm_mode = True
        allow_population_by_field_name = True
