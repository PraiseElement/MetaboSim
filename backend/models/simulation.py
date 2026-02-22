"""
Pydantic request/response models for the MetaboSim simulation API.
"""
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from pydantic import ConfigDict


class SimulationRequest(BaseModel):
    """Parameters provided by the user to run a simulation."""
    pathway: str = Field(
        default="glycolysis",
        description="Which pathway to simulate"
    )
    glucose_mM: float = Field(default=5.0, ge=0.0, le=25.0, description="Blood glucose in mM (normal ~5 mM)")
    oxygen_pct: float = Field(default=100.0, ge=0.0, le=100.0, description="O2 availability as percentage of normal")
    insulin_fold: float = Field(default=1.0, ge=0.0, le=5.0, description="Insulin level fold change vs basal")
    glucagon_fold: float = Field(default=1.0, ge=0.0, le=5.0, description="Glucagon level fold change vs basal")
    energy_demand: float = Field(default=1.0, ge=0.1, le=5.0, description="Energy demand multiplier (1x=rest, 5x=heavy exercise)")
    nutritional_state: str = Field(default="fed", description="Nutritional state: fed, fasted, starved")


class EnzymeState(BaseModel):
    """State of a single enzyme in the pathway."""
    enzyme_id: str
    enzyme_name: str
    flux: float          # relative flux 0.0 - 1.0
    activity: float      # actual activity 0.0 - 1.0
    is_regulated: bool
    regulators: List[str]
    status: str          # "active", "inhibited", "allosteric", "bypass"


class MetaboliteLevel(BaseModel):
    """Concentration of a metabolite."""
    metabolite_id: str
    name: str
    concentration: float  # relative units
    trend: str            # "rising", "falling", "stable"


class PathwayMetrics(BaseModel):
    """
    Key metrics output from a pathway simulation.
    The 8 baseline fields are always present; pathway-specific fields
    (e.g. bhb_produced, uric_acid_produced) are allowed as extras.
    """
    model_config = ConfigDict(extra="allow")

    # Baseline fields — every engine must return these
    atp_yield: float = 0.0
    nadh_produced: float = 0.0
    fadh2_produced: float = 0.0
    co2_released: float = 0.0
    net_flux: float = 0.0        # 0.0 - 1.0 (relative to max)
    pyruvate_output: float = 0.0
    lactate_output: float = 0.0
    glucose_consumed: float = 0.0

    # Common optional fields returned by multiple engines
    atp_invested: Optional[float] = 0.0
    atp_substrate_produced: Optional[float] = 0.0
    nadph_consumed: Optional[float] = 0.0
    nadph_produced: Optional[float] = 0.0


class SimulationResult(BaseModel):
    """Full simulation result returned to the frontend."""
    model_config = ConfigDict(extra="allow")

    pathway: str
    scenario_detected: str           # e.g. "hypoxia", "exercise", "normal"
    enzymes: List[EnzymeState]
    metabolites: List[MetaboliteLevel]
    metrics: PathwayMetrics
    educational_notes: List[str]
    warnings: List[str]
