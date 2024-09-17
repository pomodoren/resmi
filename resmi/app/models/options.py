import enum


class StandardQuality(enum.Enum):
    VERY_GOOD = "Very good"
    GOOD = "Good"
    NEEDS_REPAIR = "Needs repair"
    PROBLEMATIC = "Problematic"
    NON_EXISTENT = "Non-existent"


class StandardPresence(enum.Enum):
    PRESENT = "Present"
    PRESENT_NEEDS_REPAIR = "Present, needs repair"
    PRESENT_NEEDS_CHANGING = "Present, needs changing"
    NOT_PRESENT = "Not present"


class MaterialType(enum.Enum):
    METAL = "Metal"
    WOOD = "Wood"
    PLASTIC = "Plastic"
    CONCRETE = "Concrete"


class VisibilityLevel(enum.Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
    NONE = "None"


class Status(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    UNDER_CONSTRUCTION = "Under Construction"
    PLANNED = "Planned"


class Accessibility(enum.Enum):
    FULLY_ACCESSIBLE = "Fully Accessible"
    PARTIALLY_ACCESSIBLE = "Partially Accessible"
    NOT_ACCESSIBLE = "Not Accessible"


class SurfaceType(enum.Enum):
    ASPHALT = "Asphalt"
    CONCRETE = "Concrete"
    GRAVEL = "Gravel"
    DIRT = "Dirt"


class TrafficFlow(enum.Enum):
    ONE_WAY = "One Way"
    TWO_WAY = "Two Way"


class ActivityStatus(enum.Enum):
    DEFINED = "Defined"
    STARTED = "Started"
    MIDWAY = "Midway"
    ALMOST = "Almost done"
    DONE = "Done"
    POSTPONED = "Postponed"
    DISMISSED = "Dismissed"


class DepreciationType(enum.Enum):
    LINEAR = "Linear"
    EXPONENTIAL = "Exponential"
    DOUBLE_DECLINING = "Double Declining"
    STRAIGHT_LINE = "Straight Line"


class CostUnitType(enum.Enum):
    PER_UNIT_DOLLAR = "Per Unit in $"
    PER_UNIT_ALL = "Per Unit in ALL"
    TOTAL_DOLLAR = "Total $"
    TOTAL_ALL = "Total ALL"


class ConditionCheck(enum.Enum):
    CHECKED_TRUE = "Checked True"
    CHECKED_FALSE = "Checked False"
    NOT_CHECKED = "Not Checked"
    NOT_APPLICABLE = "Not Applicable"
