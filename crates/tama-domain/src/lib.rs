#![no_std]
#![forbid(unsafe_code)]

/// Elapsed monotonic time supplied by the application loop.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub struct ElapsedMillis(u32);

impl ElapsedMillis {
    pub const fn new(value: u32) -> Self {
        Self(value)
    }

    pub const fn get(self) -> u32 {
        self.0
    }
}

/// Hardware-independent input consumed by application and domain logic.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
pub enum InputEvent {
    RotateLeft,
    RotateRight,
    Confirm,
    Back,
    Tick(ElapsedMillis),
}
