import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdateManagementComponent } from './update-management.component';

describe('UpdateManagementComponent', () => {
  let component: UpdateManagementComponent;
  let fixture: ComponentFixture<UpdateManagementComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ UpdateManagementComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdateManagementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
