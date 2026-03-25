import clsx from "clsx";
import svgPaths from "./svg-hfhi0zz7rh";
import imgAbstractAiArchitecture from "figma:asset/3f53dd22dd851dbc075025cdfbe17f663af50926.png";
import imgUserProfile from "figma:asset/ba52c19535cd4d6f97f3ffd683a3bf037db144a2.png";

function Container1({ children }: React.PropsWithChildren<{}>) {
  return (
    <div className="h-[20px] relative shrink-0 w-[20.1px]">
      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20.1 20">
        <g id="Container">{children}</g>
      </svg>
    </div>
  );
}

function Container({ children }: React.PropsWithChildren<{}>) {
  return (
    <div className="relative shrink-0 size-[18px]">
      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 18 18">
        <g id="Container">{children}</g>
      </svg>
    </div>
  );
}
type WrapperProps = {
  additionalClassNames?: string;
};

function Wrapper({ children, additionalClassNames = "" }: React.PropsWithChildren<WrapperProps>) {
  return (
    <div className={clsx("relative rounded-[48px] shrink-0 w-full", additionalClassNames)}>
      <div className="flex flex-row items-center size-full">
        <div className="content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative w-full">{children}</div>
      </div>
    </div>
  );
}

function Margin() {
  return (
    <div className="relative self-stretch shrink-0">
      <div className="flex flex-col justify-center size-full">
        <div className="content-stretch flex flex-col h-full items-start justify-center pt-[4px] relative">
          <div className="content-stretch flex flex-[1_0_0] flex-col items-start min-h-px min-w-px relative">
            <div className="relative shrink-0 size-[11.667px]" data-name="Icon">
              <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 11.6667 11.6667">
                <path d={svgPaths.p1d9bcc00} fill="var(--fill-0, #005DAA)" id="Icon" />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default function Body() {
  return (
    <div className="bg-[#f8f9fa] content-stretch flex flex-col items-start relative size-full" data-name="Body">
      <div className="content-stretch flex h-[1024px] isolate items-start relative shrink-0 w-full" data-name="Container">
        <div className="bg-[#f8f9fa] h-full relative shrink-0 w-[256px] z-[2]" data-name="Aside - SideNavBar Component">
          <div className="content-stretch flex flex-col gap-[8px] items-start p-[16px] relative size-full">
            <div className="content-stretch flex flex-col items-start pb-[16px] relative shrink-0 w-full" data-name="Margin">
              <div className="relative shrink-0 w-full" data-name="Container">
                <div className="flex flex-row items-center size-full">
                  <div className="content-stretch flex gap-[12px] items-center px-[8px] py-[24px] relative w-full">
                    <div className="bg-[#005daa] content-stretch flex items-center justify-center relative rounded-[48px] shrink-0 size-[40px]" data-name="Background">
                      <div className="-translate-y-1/2 absolute bg-[rgba(255,255,255,0)] left-0 rounded-[48px] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)] size-[40px] top-1/2" data-name="Overlay+Shadow" />
                      <div className="h-[16px] relative shrink-0 w-[17.7px]" data-name="Container">
                        <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 17.7 16">
                          <g id="Container">
                            <path d={svgPaths.p19386c00} fill="var(--fill-0, white)" id="Icon" />
                          </g>
                        </svg>
                      </div>
                    </div>
                    <div className="content-stretch flex flex-col items-start relative shrink-0 w-[83.59px]" data-name="Container">
                      <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 1">
                        <div className="flex flex-col font-['Liberation_Serif:Bold',sans-serif] h-[28px] justify-center leading-[0] not-italic relative shrink-0 text-[#373cff] text-[18px] tracking-[-0.45px] w-[83.59px]">
                          <p className="leading-[28px]">Intelligence</p>
                        </div>
                      </div>
                      <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
                        <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[#94a3b8] text-[10px] tracking-[1px] uppercase w-[80.11px]">
                          <p className="leading-[15px]">Monolith V1</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="content-stretch flex flex-[1_0_0] flex-col gap-[4px] items-start min-h-px min-w-px relative w-full" data-name="Nav">
              <Wrapper additionalClassNames="bg-white shadow-[0px_1px_2px_0px_rgba(0,0,0,0.05)]">
                <div className="relative shrink-0 size-[14px]" data-name="Container">
                  <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 14">
                    <g id="Container">
                      <path d={svgPaths.p2bb32400} fill="var(--fill-0, #373CFF)" id="Icon" />
                    </g>
                  </svg>
                </div>
                <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                  <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#373cff] text-[14px] text-center w-[65.33px]">
                    <p className="leading-[20px]">New Chat</p>
                  </div>
                </div>
              </Wrapper>
              <Wrapper>
                <Container>
                  <path d={svgPaths.p22876fc0} fill="var(--fill-0, #475569)" id="Icon" />
                </Container>
                <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                  <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#475569] text-[14px] text-center w-[110.63px]">
                    <p className="leading-[20px]">Recent Sessions</p>
                  </div>
                </div>
              </Wrapper>
              <Wrapper>
                <div className="h-[18px] relative shrink-0 w-[14px]" data-name="Container">
                  <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 14 18">
                    <g id="Container">
                      <path d={svgPaths.p1db08b60} fill="var(--fill-0, #475569)" id="Icon" />
                    </g>
                  </svg>
                </div>
                <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                  <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#475569] text-[14px] text-center w-[101.03px]">
                    <p className="leading-[20px]">Saved Prompts</p>
                  </div>
                </div>
              </Wrapper>
              <Wrapper>
                <Container>
                  <path d={svgPaths.pf86ae00} fill="var(--fill-0, #475569)" id="Icon" />
                </Container>
                <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                  <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#475569] text-[14px] text-center w-[51.11px]">
                    <p className="leading-[20px]">Archive</p>
                  </div>
                </div>
              </Wrapper>
            </div>
            <div className="content-stretch flex flex-col gap-[16px] items-start pt-[17px] relative shrink-0 w-full" data-name="HorizontalBorder">
              <div aria-hidden="true" className="absolute border-[#e2e8f0] border-solid border-t inset-0 pointer-events-none" />
              <div className="bg-[#1a76cf] relative rounded-[16px] shrink-0 w-full" data-name="Background">
                <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col gap-[8px] items-start p-[16px] relative w-full">
                  <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
                    <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[#fefcff] text-[12px] w-full">
                      <p className="leading-[16px]">Upgrade to Pro</p>
                    </div>
                  </div>
                  <div className="content-stretch flex flex-col items-start opacity-70 pb-[4px] relative shrink-0 w-full" data-name="Container">
                    <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[16.25px] not-italic relative shrink-0 text-[#fefcff] text-[10px] w-full">
                      <p className="mb-0">Unlock advanced architectural</p>
                      <p>reasoning and unlimited contexts.</p>
                    </div>
                  </div>
                  <div className="bg-[#005daa] content-stretch flex items-center justify-center py-[8px] relative rounded-[32px] shrink-0 w-full" data-name="Button">
                    <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[16px] justify-center leading-[0] not-italic relative shrink-0 text-[12px] text-center text-white w-[50.34px]">
                      <p className="leading-[16px]">Upgrade</p>
                    </div>
                  </div>
                </div>
              </div>
              <div className="relative rounded-[48px] shrink-0 w-full" data-name="Button">
                <div className="flex flex-row items-center size-full">
                  <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[12px] items-center px-[16px] py-[12px] relative w-full">
                    <Container1>
                      <path d={svgPaths.p3cdadd00} fill="var(--fill-0, #475569)" id="Icon" />
                    </Container1>
                    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#475569] text-[14px] text-center w-[54.92px]">
                        <p className="leading-[20px]">Settings</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div className="relative rounded-[48px] shrink-0 w-full" data-name="Button">
                <div className="flex flex-row items-center size-full">
                  <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex gap-[12px] items-center pb-[12px] px-[16px] relative w-full">
                    <Container>
                      <path d={svgPaths.p3e9df400} fill="var(--fill-0, #475569)" id="Icon" />
                    </Container>
                    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                      <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[20px] justify-center leading-[0] not-italic relative shrink-0 text-[#475569] text-[14px] text-center w-[46.7px]">
                        <p className="leading-[20px]">Logout</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div className="bg-[#f9f9ff] flex-[1_0_0] h-full min-h-px min-w-px overflow-clip relative z-[1]" data-name="Main Content Area">
          <div className="absolute content-stretch flex flex-col gap-[48px] inset-[72px_0_-591.5px_0] items-start max-w-[1024px] px-[48px] py-[32px]" data-name="Section - Chat Canvas">
            <div className="content-stretch flex flex-col items-start pb-[48px] pt-[80px] relative shrink-0 w-[618.66px]" data-name="Welcome State / Empty Canvas:margin">
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-name="Welcome State / Empty Canvas">
                <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 3">
                  <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[#181c21] text-[48px] tracking-[-1.2px] w-full">
                    <p className="mb-0">
                      <span className="leading-[48px]">{`The architecture of `}</span>
                      <span className="font-['Inter:Bold',sans-serif] font-bold leading-[48px] not-italic text-[#005daa]">pure</span>
                    </p>
                    <p>
                      <span className="font-['Inter:Bold',sans-serif] font-bold leading-[48px] not-italic text-[#005daa]">thought</span>
                      <span className="leading-[48px]">.</span>
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Container">
                  <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[29.25px] not-italic relative shrink-0 text-[#414752] text-[18px] w-full">
                    <p className="mb-0">How can I assist your creative or analytical process today? Our models</p>
                    <p>are optimized for precision and clarity.</p>
                  </div>
                </div>
                <div className="gap-x-[16px] gap-y-[16px] grid grid-cols-[repeat(2,minmax(0,1fr))] grid-rows-[_158px] pt-[24px] relative shrink-0 w-full" data-name="Suggested Actions Bento Grid">
                  <div className="bg-white col-1 h-[158px] justify-self-stretch relative rounded-[16px] row-1 shrink-0" data-name="Background+Border">
                    <div aria-hidden="true" className="absolute border border-[rgba(193,199,212,0.1)] border-solid inset-0 pointer-events-none rounded-[16px]" />
                    <div className="absolute bg-[rgba(255,255,255,0)] inset-0 rounded-[16px] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" data-name="Overlay+Shadow" />
                    <div className="absolute left-[26px] size-[22px] top-[26px]" data-name="Icon">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 22 22">
                        <path d={svgPaths.p11c2d500} fill="var(--fill-0, #005DAA)" id="Icon" />
                      </svg>
                    </div>
                    <div className="absolute content-stretch flex flex-col items-start left-[25px] right-[25px] top-[61px]" data-name="Heading 4">
                      <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[24px] justify-center leading-[0] not-italic relative shrink-0 text-[#181c21] text-[16px] w-[142.39px]">
                        <p className="leading-[24px]">Strategic Analysis</p>
                      </div>
                    </div>
                    <div className="absolute content-stretch flex flex-col items-start left-[25px] right-[25px] top-[93px]" data-name="Container">
                      <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal h-[40px] justify-center leading-[20px] not-italic relative shrink-0 text-[#414752] text-[14px] w-[248.63px]">
                        <p className="mb-0">Review a business model and identify</p>
                        <p>architectural weaknesses.</p>
                      </div>
                    </div>
                  </div>
                  <div className="bg-white col-2 h-[158px] justify-self-stretch relative rounded-[16px] row-1 shrink-0" data-name="Background+Border">
                    <div aria-hidden="true" className="absolute border border-[rgba(193,199,212,0.1)] border-solid inset-0 pointer-events-none rounded-[16px]" />
                    <div className="absolute bg-[rgba(255,255,255,0)] inset-0 rounded-[16px] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" data-name="Overlay+Shadow" />
                    <div className="absolute h-[12px] left-[27px] top-[31px] w-[20px]" data-name="Icon">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 12">
                        <path d={svgPaths.p24c05900} fill="var(--fill-0, #005DAA)" id="Icon" />
                      </svg>
                    </div>
                    <div className="absolute content-stretch flex flex-col items-start left-[25px] right-[25px] top-[61px]" data-name="Heading 4">
                      <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[24px] justify-center leading-[0] not-italic relative shrink-0 text-[#181c21] text-[16px] w-[136.19px]">
                        <p className="leading-[24px]">Code Refactoring</p>
                      </div>
                    </div>
                    <div className="absolute content-stretch flex flex-col items-start left-[25px] right-[25px] top-[93px]" data-name="Container">
                      <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal h-[40px] justify-center leading-[20px] not-italic relative shrink-0 text-[#414752] text-[14px] w-[212.3px]">
                        <p className="mb-0">Analyze existing repositories for</p>
                        <p>performance and elegance.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="content-stretch flex flex-col gap-[48px] items-start pb-[128px] relative shrink-0 w-full" data-name="Chat History Start (Example Conversation)">
              <div className="content-stretch flex flex-col items-end relative shrink-0 w-full" data-name="User Message">
                <div className="bg-white content-stretch flex flex-col items-start max-w-[603.2000122070312px] pl-[21px] pr-[87.03px] py-[21px] relative rounded-bl-[24px] rounded-br-[24px] rounded-tl-[24px] shrink-0" data-name="Background+Border">
                  <div aria-hidden="true" className="absolute border border-[rgba(193,199,212,0.05)] border-solid inset-0 pointer-events-none rounded-bl-[24px] rounded-br-[24px] rounded-tl-[24px]" />
                  <div className="absolute bg-[rgba(255,255,255,0)] inset-0 shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" data-name="Overlay+Shadow" />
                  <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal h-[78px] justify-center leading-[26px] not-italic relative shrink-0 text-[#181c21] text-[16px] w-[495.16px]">
                    <p className="mb-0">{`Can you explain the concept of "Intelligent Monoliths" in software`}</p>
                    <p className="mb-0">architecture and how it contrasts with microservices in terms of</p>
                    <p>maintainability?</p>
                  </div>
                </div>
                <div className="content-stretch flex flex-col items-start pt-[8px] px-[8px] relative shrink-0" data-name="Margin">
                  <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[#94a3b8] text-[10px] tracking-[-0.5px] uppercase w-[70.84px]">
                    <p className="leading-[15px]">You • 10:24 AM</p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[24px] items-start relative shrink-0 w-full" data-name="AI Response">
                <div className="content-stretch flex gap-[16px] items-start relative shrink-0 w-full" data-name="Container">
                  <div className="bg-[#005daa] content-stretch flex items-center justify-center pb-[9px] pt-[8px] relative rounded-[32px] shrink-0 size-[32px]" data-name="Background">
                    <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[10px] text-center text-white w-[12.13px]">
                      <p className="leading-[15px]">IM</p>
                    </div>
                  </div>
                  <div className="bg-[#f2f3fb] max-w-[696px] relative rounded-bl-[24px] rounded-br-[24px] rounded-tr-[24px] self-stretch shrink-0 w-[696px]" data-name="Background+Border">
                    <div aria-hidden="true" className="absolute border border-[rgba(255,255,255,0.4)] border-solid inset-0 pointer-events-none rounded-bl-[24px] rounded-br-[24px] rounded-tr-[24px]" />
                    <div className="content-stretch flex flex-col items-start max-w-[inherit] p-[33px] relative size-full">
                      <div className="absolute bg-[rgba(255,255,255,0)] inset-0 shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" data-name="Overlay+Shadow" />
                      <div className="relative shrink-0 w-full" data-name="Container">
                        <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col gap-[16px] items-start relative w-full">
                          <div className="content-stretch flex flex-col items-start relative shrink-0 w-full" data-name="Heading 5">
                            <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold justify-center leading-[0] not-italic relative shrink-0 text-[#181c21] text-[18px] w-full">
                              <p className="leading-[28px]">The Monolithic Shift</p>
                            </div>
                          </div>
                          <div className="h-[78px] not-italic relative shrink-0 text-[#181c21] text-[16px] w-full" data-name="Container">
                            <div className="-translate-y-1/2 absolute flex flex-col font-['Inter:Regular',sans-serif] font-normal h-[52px] justify-center leading-[26px] left-0 top-[26px] w-[625.25px]">
                              <p className="mb-0">{`An "Intelligent Monolith" refers to a unified system where components are logically`}</p>
                              <p>{`separated but physically co-located. This design philosophy emphasizes `}</p>
                            </div>
                            <div className="absolute font-['Inter:Bold',sans-serif] font-bold h-[46px] leading-[0] left-0 top-[29px] w-[619px]" data-name="Strong">
                              <div className="-translate-y-1/2 absolute flex flex-col h-[26px] justify-center left-[554.27px] top-[10px] w-[64.73px]">
                                <p className="leading-[26px]">reduced</p>
                              </div>
                              <div className="-translate-y-1/2 absolute flex flex-col h-[26px] justify-center left-0 top-[36px] w-[150.61px]">
                                <p className="leading-[26px]">cognitive overhead</p>
                              </div>
                            </div>
                            <div className="-translate-y-1/2 absolute flex flex-col font-['Inter:Regular',sans-serif] font-normal h-[26px] justify-center leading-[0] left-[150.61px] top-[65px] w-[267.38px]">
                              <p className="leading-[26px]">{` over extreme horizontal scalability.`}</p>
                            </div>
                          </div>
                          <div className="content-stretch flex flex-col gap-[12px] items-start relative shrink-0 w-full" data-name="List">
                            <div className="content-stretch flex gap-[12px] h-[40px] items-start relative shrink-0 w-full" data-name="Item">
                              <Margin />
                              <div className="content-stretch flex flex-col items-start pr-[31.14px] relative self-stretch shrink-0" data-name="Container">
                                <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[40px] justify-center leading-[0] not-italic relative shrink-0 text-[#414752] text-[14px] w-[572.84px]">
                                  <p className="mb-0">
                                    <span className="leading-[20px]">Maintainability:</span>
                                    <span className="font-['Inter:Regular',sans-serif] font-normal leading-[20px] not-italic">{` Single deployment pipelines eliminate the "version hell" often found in`}</span>
                                  </p>
                                  <p className="font-['Inter:Regular',sans-serif] font-normal leading-[20px]">service meshes.</p>
                                </div>
                              </div>
                            </div>
                            <div className="content-stretch flex gap-[12px] h-[40px] items-start relative shrink-0 w-full" data-name="Item">
                              <Margin />
                              <div className="content-stretch flex flex-col items-start pr-[2.39px] relative self-stretch shrink-0" data-name="Container">
                                <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[40px] justify-center leading-[0] not-italic relative shrink-0 text-[#414752] text-[14px] w-[601.59px]">
                                  <p className="mb-0">
                                    <span className="leading-[20px]">Performance:</span>
                                    <span className="font-['Inter:Regular',sans-serif] font-normal leading-[20px] not-italic">{` In-process communication avoids the 10-50ms latency overhead of network`}</span>
                                  </p>
                                  <p className="font-['Inter:Regular',sans-serif] font-normal leading-[20px]">calls.</p>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div className="content-stretch flex flex-col h-[200px] items-start justify-center overflow-clip pt-[8px] relative rounded-[48px] shrink-0 w-full" data-name="Container">
                            <div className="flex-[1_0_0] min-h-px min-w-px relative w-full" data-name="Abstract AI architecture">
                              <div className="absolute inset-0 overflow-hidden pointer-events-none">
                                <img alt="" className="absolute h-[328.12%] left-0 max-w-none top-[-114.06%] w-full" src={imgAbstractAiArchitecture} />
                              </div>
                            </div>
                          </div>
                          <div className="content-stretch flex flex-col items-start pt-[8px] relative shrink-0 w-full" data-name="Container">
                            <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[26px] not-italic relative shrink-0 text-[#181c21] text-[16px] w-full">
                              <p className="mb-0">Contrast this with microservices, which offer high fault isolation but introduce</p>
                              <p>massive complexity in observability and transactional consistency.</p>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="content-stretch flex flex-col items-start pl-[48px] relative shrink-0" data-name="Margin">
                  <div className="content-stretch flex gap-[16px] items-center relative shrink-0" data-name="Container">
                    <div className="h-[11.667px] relative shrink-0 w-[12.25px]" data-name="Button">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12.25 11.6667">
                        <g id="Button">
                          <path d={svgPaths.p1fd12b00} fill="var(--fill-0, #94A3B8)" id="Icon" />
                        </g>
                      </svg>
                    </div>
                    <div className="h-[11.667px] relative shrink-0 w-[9.917px]" data-name="Button">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 9.91667 11.6667">
                        <g id="Button">
                          <path d={svgPaths.p29eb9000} fill="var(--fill-0, #94A3B8)" id="Icon" />
                        </g>
                      </svg>
                    </div>
                    <div className="h-[11.667px] relative shrink-0 w-[10.5px]" data-name="Button">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 10.5 11.6667">
                        <g id="Button">
                          <path d={svgPaths.p313c6040} fill="var(--fill-0, #94A3B8)" id="Icon" />
                        </g>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="absolute backdrop-blur-[10px] bg-[rgba(255,255,255,0.8)] bottom-0 content-stretch flex flex-col gap-[12px] items-center left-0 pb-[32px] pt-[33px] px-[32px] right-0" data-name="Command Bar (Input)">
            <div aria-hidden="true" className="absolute border-[rgba(193,199,212,0.1)] border-solid border-t inset-0 pointer-events-none" />
            <div className="max-w-[896px] relative shrink-0 w-[896px]" data-name="Container">
              <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-start max-w-[inherit] relative w-full">
                <div className="bg-[rgba(224,226,234,0.5)] relative rounded-[16px] shrink-0 w-full" data-name="Input">
                  <div className="flex flex-row justify-center overflow-clip rounded-[inherit] size-full">
                    <div className="content-stretch flex items-start justify-center pb-[24px] pl-[56px] pr-[128px] pt-[23px] relative w-full">
                      <div className="content-stretch flex flex-[1_0_0] flex-col items-start min-h-px min-w-px overflow-clip relative" data-name="Container">
                        <div className="flex flex-col font-['Inter:Regular',sans-serif] font-normal justify-center leading-[0] not-italic relative shrink-0 text-[#94a3b8] text-[18px] w-full">
                          <p className="leading-[normal]">Describe your inquiry...</p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="absolute bottom-0 content-stretch flex items-center left-[20px] top-0" data-name="Container">
                  <div className="content-stretch flex flex-col items-center justify-center relative shrink-0" data-name="Button">
                    <div className="h-[20px] relative shrink-0 w-[12.5px]" data-name="Container">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 12.5 20">
                        <g id="Container">
                          <path d={svgPaths.p2fe31000} fill="var(--fill-0, #94A3B8)" id="Icon" />
                        </g>
                      </svg>
                    </div>
                  </div>
                </div>
                <div className="absolute bottom-[8px] content-stretch flex items-center right-[8px] top-[8px]" data-name="Container">
                  <div className="bg-[#005daa] content-stretch flex gap-[8px] h-full items-center px-[24px] relative rounded-[48px] shrink-0" data-name="Button">
                    <div className="absolute bg-[rgba(255,255,255,0)] inset-[0_0.06px_0_0] rounded-[48px] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" data-name="Button:shadow" />
                    <div className="content-stretch flex flex-col items-center relative shrink-0" data-name="Container">
                      <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[24px] justify-center leading-[0] not-italic relative shrink-0 text-[16px] text-center text-white w-[40.06px]">
                        <p className="leading-[24px]">Send</p>
                      </div>
                    </div>
                    <div className="h-[9.333px] relative shrink-0 w-[11.083px]" data-name="Container">
                      <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 11.0833 9.33333">
                        <g id="Container">
                          <path d={svgPaths.pfe16e10} fill="var(--fill-0, white)" id="Icon" />
                        </g>
                      </svg>
                    </div>
                  </div>
                </div>
                <div className="absolute content-stretch flex gap-[8px] items-center left-0 top-[-32px]" data-name="AI Status Indicator">
                  <div className="bg-[#005daa] relative rounded-[9999px] shrink-0 size-[6px]" data-name="Background">
                    <div className="absolute bg-[#005daa] blur-[1px] inset-0 rounded-[9999px]" data-name="Background+Blur" />
                  </div>
                  <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
                    <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[#94a3b8] text-[10px] tracking-[1px] uppercase w-[125.7px]">
                      <p className="leading-[15px]">Awaiting Command</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div className="relative shrink-0 w-full" data-name="Container">
              <div className="bg-clip-padding border-0 border-[transparent] border-solid content-stretch flex flex-col items-center relative w-full">
                <div className="flex flex-col font-['Inter:Medium',sans-serif] font-medium h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[#94a3b8] text-[10px] text-center w-[236.75px]">
                  <p className="leading-[15px]">Model: Monolith-v1-Turbo • Context: 128k Tokens</p>
                </div>
              </div>
            </div>
          </div>
          <div className="absolute bg-gradient-to-b content-stretch flex from-white items-center justify-between left-0 px-[32px] py-[16px] right-0 to-[#f8f9fa] top-0" data-name="Header - TopAppBar Component">
            <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Heading 2">
              <div className="flex flex-col font-['Liberation_Serif:Bold',sans-serif] h-[28px] justify-center leading-[0] not-italic relative shrink-0 text-[#373cff] text-[20px] tracking-[-1px] w-[151.67px]">
                <p className="leading-[28px]">Intelligent Monolith</p>
              </div>
            </div>
            <div className="content-stretch flex gap-[16.01px] items-center relative shrink-0" data-name="Container">
              <div className="bg-[#f2f3fb] content-stretch flex gap-[8px] items-center px-[12px] py-[4px] relative rounded-[9999px] shrink-0" data-name="Background">
                <div className="bg-[#005daa] relative rounded-[9999px] shrink-0 size-[8px]" data-name="Background">
                  <div className="absolute bg-[#005daa] inset-0 opacity-25 rounded-[9999px]" data-name="Background" />
                </div>
                <div className="content-stretch flex flex-col items-start relative shrink-0" data-name="Container">
                  <div className="flex flex-col font-['Inter:Bold',sans-serif] font-bold h-[15px] justify-center leading-[0] not-italic relative shrink-0 text-[#64748b] text-[10px] tracking-[1px] uppercase w-[95.23px]">
                    <p className="leading-[15px]">System Active</p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex gap-[8px] items-center relative shrink-0" data-name="Container">
                <div className="content-stretch flex flex-col items-center justify-center p-[8px] relative shrink-0" data-name="Button">
                  <div className="relative shrink-0 size-[20px]" data-name="Container">
                    <svg className="absolute block size-full" fill="none" preserveAspectRatio="none" viewBox="0 0 20 20">
                      <g id="Container">
                        <path d={svgPaths.p2816f2c0} fill="var(--fill-0, #64748B)" id="Icon" />
                      </g>
                    </svg>
                  </div>
                </div>
                <div className="content-stretch flex flex-col items-center justify-center p-[8px] relative shrink-0" data-name="Button">
                  <Container1>
                    <path d={svgPaths.p3cdadd00} fill="var(--fill-0, #64748B)" id="Icon" />
                  </Container1>
                </div>
                <div className="content-stretch flex flex-col h-[32px] items-start pl-[8px] relative shrink-0 w-[40px]" data-name="Margin">
                  <div className="bg-[rgba(255,255,255,0)] relative rounded-[9999px] shrink-0 size-[32px]" data-name="Overlay+Border+Shadow">
                    <div className="content-stretch flex flex-col items-start justify-center overflow-clip p-px relative rounded-[inherit] size-full">
                      <div className="flex-[1_0_0] min-h-px min-w-px relative w-full" data-name="User profile">
                        <div className="absolute bg-clip-padding border-0 border-[transparent] border-solid inset-0 overflow-hidden pointer-events-none">
                          <img alt="" className="absolute left-0 max-w-none size-full top-0" src={imgUserProfile} />
                        </div>
                      </div>
                    </div>
                    <div aria-hidden="true" className="absolute border border-solid border-white inset-0 pointer-events-none rounded-[9999px] shadow-[0px_32px_64px_-12px_rgba(43,52,55,0.06)]" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}